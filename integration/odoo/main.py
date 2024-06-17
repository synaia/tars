import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from dotenv import dotenv_values
import odoorpc
import applicant as applicant
import recording as recording

import uvicorn
import time

password = dotenv_values('.secret')['PASSWORD']
params = dotenv_values('.env')
react_origin = f"http://{params['HOST']}:{params['R_PORT']}"

origins = [
    react_origin, # react-app
]

# Prepare the connection to the server
odoo = odoorpc.ODOO(params['ODOO_SRV'], port=params['PORT'], protocol='jsonrpc+ssl')


@asynccontextmanager
async def lifespan(app: FastAPI):
   print('init lifespan ...')
   odoo.login(params['DB'], params['USER'], password)
   app.state.odoo = odoo
   yield
   print('bye application')

app = FastAPI(lifespan=lifespan)
app.include_router(applicant.router)
app.include_router(recording.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# debug mode :-)
if __name__ == "__main__":
    uvicorn.run(app, host=params['F_HOST'], port=params['F_PORT'],)

app.mount("/", StaticFiles(directory="../../recruitment/prescreening/build", html=True), name="build")
