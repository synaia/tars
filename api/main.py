import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from dotenv import dotenv_values
from samantha.src.machinery import DataManager, redis_conn

import webhook as webhook
import llm_service as llm_service

import uvicorn


def phoenix_debug():
    import phoenix as px

    phoenix_session = px.launch_app()

    from openinference.instrumentation.dspy import DSPyInstrumentor
    from opentelemetry import trace as trace_api
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk import trace as trace_sdk
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor

    endpoint = "http://127.0.0.1:6006/v1/traces"
    resource = Resource(attributes={})
    tracer_provider = trace_sdk.TracerProvider(resource=resource)
    span_otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
    tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter=span_otlp_exporter))

    trace_api.set_tracer_provider(tracer_provider=tracer_provider)
    DSPyInstrumentor().instrument()

    print(phoenix_session.url)


@asynccontextmanager
async def lifespan(app: FastAPI):
   secret = dotenv_values(".secret")
   app.state.secret = secret
   DataManager().data_mem_loader()
   phoenix_debug()
   yield
   redis_conn.flushdb()
   #TODO: AND CLEAN MEMORY HERE !!!
   # - destroy in memory history
   print('bye webhook application')


app = FastAPI(lifespan=lifespan)
app.include_router(webhook.router)
app.include_router(llm_service.router)

@app.get("/")
def I_am_alive():
    return "I am alive!!"


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# debug mode :-)
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9091,)

