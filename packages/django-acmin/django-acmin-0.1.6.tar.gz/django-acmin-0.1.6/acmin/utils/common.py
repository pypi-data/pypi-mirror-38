import json
import platform

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from .decorators import memorize


def to_json(data):
    return json.dumps(data, cls=DjangoJSONEncoder)


def first(l, default=None):
    return l[0] if l else default


def last(l, default=None):
    return l[len(l) - 1] if l else default


def is_windows() -> bool:
    return platform.system() == "Windows"


@memorize
def get_ip():
    if settings.DEBUG:
        return "127.0.0.1"

    with open('/data/host', 'r') as f:
        return f.readline().strip()


@memorize
def get_domain():
    if settings.DEBUG:
        return "localhost"

    with open('/data/domain', 'r') as f:
        return f.readline().strip()


def null_to_emtpy(data):
    if isinstance(data, (list, tuple)):
        return [null_to_emtpy(i) for i in data]
    if isinstance(data, dict):
        return {key: null_to_emtpy(value) for key, value in data.items()}
    if data is None:
        return ""
    return data
