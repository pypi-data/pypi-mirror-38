from typing import Dict, Type
from urllib.parse import urlparse
from datetime import datetime

from ..core import Model

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.7.1"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
__all__ = [
    "parse_couchdb_connection_uri", "serialize_datetime", "deserialize_datetime",
    "couchdb_dict_serialize", "couchdb_dict_deserialize", "CouchDBRequestException"
]

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
DDOC_FOR_GENERATED_VIEWS_NAME = "anji_orm_generated_views_ddoc"
CONNECTION_URI_MAPPING = {
    'hostname': 'host',
    'port': 'port',
    'username': 'user',
    'password': 'password',
}


class CouchDBRequestException(Exception):

    def __init__(self, query, content, status_code) -> None:
        super().__init__()
        self.query = query
        self.content = content
        self.status_code = status_code

    def __str__(self):
        return (
            f"Exception when executing query {str(self.query)}:\n"
            f"Response:{self.content}\n"
            f"Status code: {self.status_code}"
        )


def parse_couchdb_connection_uri(connection_uri: str) -> Dict:
    parsed_url = urlparse(connection_uri)
    connection_kwargs = {}
    for uri_field, connection_arg in CONNECTION_URI_MAPPING.items():
        if getattr(parsed_url, uri_field):
            connection_kwargs[connection_arg] = getattr(parsed_url, uri_field)
    if parsed_url.query:
        connection_kwargs.update({
            x[0]: x[1] for x in (x.split('=') for x in parsed_url.query.split('&'))
        })
    return connection_kwargs


def couchdb_dict_serialize(model: Type[Model], model_dict: Dict) -> None:
    model_dict['_id'] = model_dict.pop('id')
    for field_name, field in model._fields.items():
        if field.can_be(datetime) and field_name in model_dict:
            if isinstance(model_dict[field_name], datetime):
                model_dict[field_name] = serialize_datetime(model_dict[field_name])
        if field_name.startswith('_') and field_name in model_dict:
            model_dict[field_name.replace('_', '+')] = model_dict.pop(field_name)


def couchdb_dict_deserialize(model: Type[Model], model_dict: Dict) -> None:
    model_dict['id'] = model_dict.pop('_id')
    model_dict['_meta'] = {'_rev': model_dict.pop('_rev')}
    for field_name, field in model._fields.items():
        if field.can_be(datetime) and field_name in model_dict:
            if isinstance(model_dict[field_name], str):
                model_dict[field_name] = deserialize_datetime(model_dict[field_name])
        if field_name.startswith('_') and field_name.replace('_', '+') in model_dict:
            model_dict[field_name] = model_dict.pop(field_name.replace('_', '+'))


def serialize_datetime(value: datetime) -> str:
    return value.strftime(DATETIME_FORMAT)


def deserialize_datetime(value: str) -> datetime:
    return datetime.strptime(value, DATETIME_FORMAT)
