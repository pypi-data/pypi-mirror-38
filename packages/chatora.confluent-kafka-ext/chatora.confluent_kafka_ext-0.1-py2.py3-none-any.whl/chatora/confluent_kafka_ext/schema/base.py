__all__ = (
    'BaseAvroSchema',
    'avro_loads',
    'avro_load',
)

import abc
import codecs
import inspect
import io
import pathlib
import typing

from avro import schema as _avro_schema
from fastavro.schema import parse_schema as fastavro_parse_schema
from simplejson import dumps as _simplejson_dumps

from chatora.util.functional import reify


@reify
def x_py_obj(self) -> typing.Any:
    return self.to_json()


@reify
def x_json_str(self) -> str:
    return _simplejson_dumps(self.x_py_obj)


@reify
def x_fastavro_parsed_schema(self) -> typing.Any:
    return fastavro_parse_schema(self.x_py_obj)


def x__hash__(self) -> str:
    return hash(self.x_json_str)


class BaseAvroSchema(abc.ABC):
    __hash__ = x__hash__
    x_py_obj = x_py_obj
    x_json_str = x_json_str
    x_fastavro_parsed_schema = x_fastavro_parsed_schema


for n, v in _avro_schema.__dict__.items():
    if inspect.isclass(v) is True and issubclass(v, _avro_schema.Schema) is True:
        BaseAvroSchema.register(v)
        if '__hash__' not in v.__dict__ or v.__hash__ is None:
            v.__hash__ = x__hash__
        v.x_py_obj = x_py_obj
        v.x_json_str = x_json_str
        v.x_fastavro_parsed_schema = x_fastavro_parsed_schema
        if n.startswith('_') is False:
            if n not in globals():
                globals()[n] = v
            # __all__.append(n)


def avro_loads(schema_str: str) -> BaseAvroSchema:
    return _avro_schema.Parse(schema_str)


def avro_load(fp: typing.Union[typing.TextIO, pathlib.Path]) -> BaseAvroSchema:
    if isinstance(fp, io.TextIOBase) is True:
        with codecs.open(fp, mode='rt', encoding='utf-8') as f:
            return avro_loads(schema_str=f.read())
    elif isinstance(fp, pathlib.Path) is True:
        return avro_loads(schema_str=fp.read_text(encoding='utf-8'))
    else:
        raise ValueError(f'unknown src type [{fp!r}')


# __all__ = tuple(__all__)
