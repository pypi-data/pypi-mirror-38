from typing import List, Any, Iterator, Dict, Type, AsyncGenerator, Optional, Tuple
import logging
from datetime import datetime
from urllib.parse import urljoin
import re
from functools import partial

try:
    import ujson as json
    JsonFromatError: Type[Exception] = ValueError
except ImportError:
    import json  # type: ignore
    JsonFromatError: Type[Exception] = json.JSONDecodeError  # type: ignore

from ..core import (
    AbstractSyncRegisterStrategy, AbstractAsyncRegisterStrategy,
    AbstractAsyncExecutor, AbstractSyncExecutor, AbstractQueryParser, AbstractBackendAdapter,
    register, Model
)

from .executor import CouchDBAsyncExecutor, CouchDBSyncExecutor
from .parser import CouchDBQueryParser
from .utils import parse_couchdb_connection_uri, DDOC_FOR_GENERATED_VIEWS_NAME, CouchDBRequestException

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.7.3"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
__all__ = ["SyncCouchDBRegisterStrategy", "AsyncCouchDBRegisterStrategy", "CouchDBBackendAdapter"]

_log = logging.getLogger(__name__)
DDOC_INDEX_NAME_PREFIX = 'anji_orm_'
CORE_COUCHDB_METHODS = ()
SSE_LINE_PATTERN = re.compile('(?P<name>[^:]*):?( ?(?P<value>.*))?')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def _ddoc_by_index(index_name: str) -> str:
    return f"{DDOC_INDEX_NAME_PREFIX}{index_name}"


def _controlled_index_filter(index_list: List[Dict]) -> Iterator[Dict]:
    return filter(
        lambda x: x['ddoc'] is not None and DDOC_INDEX_NAME_PREFIX in x["ddoc"],
        index_list
    )


def _build_primary_index_view() -> Dict:
    return {
        "language": "query",
        "views": {
            "count": {
                "map": {
                    "fields": {"_id": "asc"},
                    "partial_filter_selector": {}
                },
                "reduce": "_count",
                "options": {"def": {"fields": ["_id"]}}
            },
        }
    }


def _controlled_index_map(index_list: List[Dict]) -> Iterator[str]:
    return map(lambda x: x["name"], _controlled_index_filter(index_list))


def parse_event_source(raw_lines: str) -> Dict:
    msg: Dict = dict()
    for line in raw_lines.splitlines():
        message_line = SSE_LINE_PATTERN.match(line)
        if message_line is None:
            # Malformed line.  Discard but warn.
            _log.warning('Invalid SSE line: "%s"', line)
            continue

        name = message_line.group('name')
        if name == '':
            # line began with a ":", so is a comment.  Ignore
            continue
        value = message_line.group('value')

        if name == 'data':
            # If we already have some data, then join to it with a newline.
            # Else this is it.
            if 'data' in msg:
                msg['data'] = '%s\n%s' % (msg['data'], value)
            else:
                try:
                    msg['data'] = json.loads(value)
                except JsonFromatError:
                    msg['data'] = value
        elif name == 'event':
            msg['event'] = value
        elif name == 'id':
            msg['id'] = value
        elif name == 'retry':
            msg['retry'] = int(value)
    return msg


async def event_stream_from_response(response, skip_heartbeat=True) -> AsyncGenerator[Dict, None]:
    lines: List[str] = []
    async for line in response.content:
        line = line.decode('utf8')

        if line in ('\n', '\r', '\r\n'):
            if not lines or lines[0] == ':ok\n':
                lines = []
                continue

            event = parse_event_source(''.join(lines))
            if not skip_heartbeat or event.get('event') != 'heartbeat':
                yield event

            lines = []
        else:
            lines.append(line)


class CouchDBBackendAdapter(AbstractBackendAdapter):

    def utcnow(self) -> datetime:
        return datetime.utcnow()

    def now(self) -> datetime:
        return datetime.now()

    @register.value_serialization(target_type=datetime)  # type: ignore
    def serialize_datetime(self, value):  # pylint: disable=no-self-use
        if value is None:
            return value
        return value.strftime(DATETIME_FORMAT)

    @register.value_deserialization(target_type=datetime)  # type: ignore
    def deserialize_datetime(self, value, result_type):  # pylint: disable=no-self-use,unused-argument
        if value is None:
            return value
        return datetime.strptime(value, DATETIME_FORMAT)

    def record_dict_serialization(self, record_dict: Dict, model_class: Type[Model]) -> Dict:
        for field_name in list(x for x in record_dict.keys() if x.startswith('_')):
            record_dict[field_name.replace('_', '+', 1)] = record_dict.pop(field_name)
        record_dict['_id'] = record_dict.pop('id')
        return record_dict

    def record_dict_deserialization(self, record_dict: Dict, model_class: Type[Model]) -> Dict:
        record_dict['id'] = record_dict.pop('_id')
        record_dict['_meta'] = {}
        if '_rev' in record_dict:
            record_dict['_meta']['_rev'] = record_dict.pop('_rev')
        for field_name in list(x for x in record_dict.keys() if '+' in x):
            record_dict[field_name.replace('+', '_', 1)] = record_dict.pop(field_name)
        return record_dict

    def fetch_processor(self, record_dict: Dict) -> Tuple[Optional[Dict], Optional[Dict]]:
        if record_dict.get('id', '').startswith('_design/anji_orm'):
            # Ignore service documentes in ORM
            return None, None

        if '+python_info' not in record_dict:
            # Return just this dict, if he cannot be recognized as orm model
            return record_dict, None
        record_dict['_python_info'] = record_dict.pop('+python_info')

        meta = {
            '_rev': record_dict.pop('_rev')
        }
        return record_dict, meta


class SyncCouchDBRegisterStrategy(AbstractSyncRegisterStrategy):

    def __init__(self, connection_uri: str, **pool_kwargs: Any) -> None:  # pylint: disable=super-init-not-called
        import requests

        self.pool = requests.Session()
        settings = parse_couchdb_connection_uri(connection_uri)
        self.base_url = f"http://{settings.get('host', '127.0.0.1')}:{settings.get('port','5984')}"
        self.url_format = partial(urljoin, self.base_url)
        self._executor = CouchDBSyncExecutor(self)
        self._query_parser = CouchDBQueryParser()
        self._backend_adapter = CouchDBBackendAdapter()

    @property
    def executor(self) -> AbstractSyncExecutor:
        return self._executor

    @property
    def query_parser(self) -> AbstractQueryParser:
        return self._query_parser

    @property
    def backend_adapter(self) -> AbstractBackendAdapter:
        return self._backend_adapter

    @property
    def db(self) -> Any:
        return self.pool

    def execute_query(self, query: Any) -> Any:
        query["url"] = self.url_format(query["url"])
        # Response from requests library not required to be closed ...
        use_stream = query.pop('grab_connection', None)
        response = self.pool.request(stream=use_stream, **query)
        if response.ok:
            if response.headers['Content-Type'] == 'text/event-stream':
                from sseclient import SSEClient
                result = SSEClient(response).events()
            elif response.headers['Content-Type'] == 'application/json':
                result = response.json()
            else:
                result = response.text
            return result
        raise CouchDBRequestException(
            query,
            response.text,
            response.status_code
        )

    def load(self) -> None:
        pass

    def create_index(
            self, table_name: str,
            index_name: str, index_fields: List[str]) -> None:
        self.execute_query({
            "method": "post",
            "url": f"{table_name}/_index",
            "json": {
                "index": {
                    "fields": index_fields
                },
                "ddoc": _ddoc_by_index(index_name),
                "name": index_name
            }
        })

    def drop_index(self, table_name: str, index_name: str) -> None:
        self.execute_query({
            "method": "delete",
            "url": f"/{table_name}/_index/{_ddoc_by_index(index_name)}/json/{index_name}"
        })

    def list_indexes(self, table_name: str) -> List[str]:
        indexes = self.execute_query({
            "method": "get",
            "url": f"/{table_name}/_index"
        })["indexes"]
        return list(_controlled_index_map(indexes))

    def create_table(self, table_name: str) -> None:
        self.execute_query({
            "method": "put",
            "url": table_name
        })
        self.execute_query({
            "method": "put",
            "url": f"{table_name}/_design/{DDOC_FOR_GENERATED_VIEWS_NAME}",
            "json": {
                "language": "javascript",
                "views": {},
                "filters": {},
                'updates': {}
            }
        })

    def drop_table(self, table_name: str) -> None:
        self.execute_query({
            "method": "delete",
            "url": f'/{table_name}'
        })

    def list_tables(self) -> List[str]:
        return self.execute_query({
            "method": "get",
            "url": '_all_dbs'
        })

    def close(self) -> None:
        self.pool.close()


class AsyncCouchDBRegisterStrategy(AbstractAsyncRegisterStrategy):

    def __init__(self, connection_uri: str, **pool_kwargs: Any) -> None:  # pylint: disable=super-init-not-called
        import aiohttp

        self.pool: aiohttp.ClientSession
        settings = parse_couchdb_connection_uri(connection_uri)
        self.base_url = f"http://{settings.get('host', '127.0.0.1')}:{settings.get('port','5984')}"
        self.url_format = partial(urljoin, self.base_url)
        self._executor = CouchDBAsyncExecutor(self)
        self._query_parser = CouchDBQueryParser()
        self._backend_adapter = CouchDBBackendAdapter()

    @property
    def executor(self) -> AbstractAsyncExecutor:
        return self._executor

    @property
    def query_parser(self) -> AbstractQueryParser:
        return self._query_parser

    @property
    def backend_adapter(self) -> AbstractBackendAdapter:
        return self._backend_adapter

    @property
    def db(self) -> Any:
        return self.pool

    async def execute_query(self, query: Any) -> Any:
        query["url"] = self.url_format(query["url"])
        grab_connection = query.pop('grab_connection', False)
        response = await self.pool.request(**query)
        if response.status >= 200 and response.status < 400:
            if response.content_type == 'text/event-stream':
                result = event_stream_from_response(response)
            elif response.content_type == 'text/html':
                result = await response.text()
            else:
                result = await response.json()
            if not grab_connection:
                response.release()
            return result
        raise CouchDBRequestException(
            query,
            await response.text(),
            response.status
        )

    async def load(self) -> None:
        import aiohttp

        self.pool = aiohttp.ClientSession()

    async def create_index(
            self, table_name: str,
            index_name: str, index_fields: List[str]) -> None:
        await self.execute_query({
            "method": "post",
            "url": f"{table_name}/_index",
            "json": {
                "index": {
                    "fields": index_fields
                },
                "ddoc": _ddoc_by_index(index_name),
                "name": index_name
            }
        })

    async def drop_index(self, table_name: str, index_name: str) -> None:
        await self.execute_query({
            "method": "delete",
            "url": f"/{table_name}/_index/{_ddoc_by_index(index_name)}/json/{index_name}"
        })

    async def list_indexes(self, table_name: str) -> List[str]:
        indexes = (await self.execute_query({
            "method": "get",
            "url": f"/{table_name}/_index"
        }))["indexes"]
        return list(_controlled_index_map(indexes))

    async def create_table(self, table_name: str) -> None:
        await self.execute_query({
            "method": "put",
            "url": table_name
        })
        await self.execute_query({
            "method": "put",
            "url": f"{table_name}/_design/{DDOC_FOR_GENERATED_VIEWS_NAME}",
            "json": {
                "language": "javascript",
                "views": {},
                'filters': {},
                'updates': {}
            }
        })

    async def drop_table(self, table_name: str) -> None:
        await self.execute_query({
            "method": "delete",
            "url": f'/{table_name}'
        })

    async def list_tables(self) -> List[str]:
        return await self.execute_query({
            "method": "get",
            "url": '_all_dbs'
        })

    async def close(self) -> None:
        await self.pool.close()
