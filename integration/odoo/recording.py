import os
import sys
from datetime import timedelta
from fastapi import Request, APIRouter, HTTPException, status, Security
from .schema import Token, Recording
from .access_token import create_access_token, validate_token, ACCESS_TOKEN_EXPIRE_SECONDS

router = APIRouter(prefix='/recording', tags=['recording'])

@router.get("/")
async def root_():
    try:
        return "hello root from recording"
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    
@router.post("/token")
async def token_(request: Request, tk: Token):
    try:
        odoo = request.app.state.odoo
        #TODO: buscar en Odoo por codigo...
        if tk.code == "20241": # dummy code for recruiter
            data = {"user": "Aurelia Matos", "user_type": "recruitment", "code": tk.code}
        elif tk.code == "20242": # dummy code for applicant
            data = {"user": "Jeferson Tejada", "user_type": "applicant", "code": tk.code}
        else:
            raise HTTPException(status_code=400, detail="Incorrect code")
        
        access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        access_token = create_access_token(
        data={"sub": data['user'], "user_type": data['user_type'], "code": data['code']},
            expires_delta=access_token_expires,
        )
        
        return {
            'access_token': access_token
        }
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    

@router.post("/push")
async def push_(request: Request, dt: Recording, token_info = Security(dependency=validate_token, scopes=["recording"])):
    try:
        return token_info
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
