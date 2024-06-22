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


@asynccontextmanager
async def lifespan(app: FastAPI):
   secret = dotenv_values(".secret")
   app.state.secret = secret
   DataManager().data_mem_loader()
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

