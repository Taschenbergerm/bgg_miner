from loguru import logger
from jaeger_client import Config

def log(func, name, *args, **kwargs):
    """
    Decorator for logging function calls.
    """
    def wrapper(*args, **kwargs):
        logger.info(f'{name} | Got called')
        res =  func(*args, **kwargs)
        logger.info(f'{name} | Finished')
        return res
    return wrapper

def configure_tracer():

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='your-app-name',
        validate=True,
    )
    # this call also sets opentracing.tracer
    tracer = config.initialize_tracer()
    return tracer

class Meta(type):
    def __new__(meta, name, bases, namespace):
        namespace_changes = {name: log(namespace[name], name) for name in namespace
                             if callable(namespace[name]) and not name.startswith('__')}

        return super().__new__(meta, name, bases, namespace | namespace_changes)


class Foo(metaclass=Meta):

    def __init__(self):
        self.name = 'Foo'

    def bar(self):
        return "bar"

if __name__ == '__main__':
    f = Foo()
    print(f.bar())