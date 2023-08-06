'''Identify scalar values in JSON and YAML documents.'''
import datetime
import sys


if sys.version_info.major == 3:
    _STRING_TYPES = (bytes, str,)
    _NUMERIC_TYPES = (int, float)
else:
    _STRING_TYPES = (str, unicode)
    _NUMERIC_TYPES = (int, long, float)


SCALAR_TYPES = sum((
    (type(None), bool, datetime.datetime), _STRING_TYPES, _NUMERIC_TYPES), ())


def is_scalar(value):
    return isinstance(value, SCALAR_TYPES)
