from opentracing.ext import tags
from opentracing.propagation import Format
from jaeger_client import Config
import opentracing


def init_tracer(service):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()



def test_new_trace():
    tracer = init_tracer("trace-my-ass")

    span = tracer.start_span(operation_name='test')
    span.set_baggage_item('Fry', 'Leela')
    span.set_tag('x', 'y')
    span.log_event('z')

    child = tracer.start_span(operation_name='child',
                              references=opentracing.child_of(span.context))
    child.log_event('w')
    carrier = {}
    tracer.inject(
        span_context=child.context, format=Format.TEXT_MAP, carrier=carrier)
    child.finish()
    span.finish()


def read_carrier():
    carrier = {'uber-trace-id': '2e87167ba473a117:dbac24813f6d2345:89a08938ac9c3db9:1', 'uberctx-Fry': 'Leela'}
    tracer = init_tracer("trace-my-ass-2")
    span_ctx = tracer.extract(format=Format.TEXT_MAP, carrier=carrier)
    span = tracer.start_span(operation_name='test',
                             references=opentracing.child_of(span_ctx))
    span.set_tag('x', 'y')
    span.set_baggage_item('a', 'b')
    span.log_event('z')
    span.finish()


if __name__ == '__main__':
    read_carrier()