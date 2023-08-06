from notedlib.output.adapter.plain import Plain
from notedlib.output.adapter.json import JSON

from notedlib.exception import NoSuchAdapterException

adapters = {
    'plain': Plain(),
    'json': JSON(),
}

# Set default adapter
adapter = adapters['plain']


def data(data):
    print(adapter.data(data))


def info(message: str):
    print(adapter.info(message))


def error(message: str, trace=None):
    print(adapter.error(message, trace))


def set_adapter(adapter_name: str):
    global adapter

    if adapter_name not in adapters:
        raise NoSuchAdapterException('No such adapter: %s' % adapter_name)

    adapter = adapters[adapter_name]
