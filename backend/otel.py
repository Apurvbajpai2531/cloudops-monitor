from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_otel(app):
    FastAPIInstrumentor.instrument_app(app)
