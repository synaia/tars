import os
import datetime
from typing import List
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from dotenv import dotenv_values
from samantha.src.dspy_models import Draft, New, Evaluation, Recording
from samantha.src.configs import odoo_message

router = APIRouter(prefix='/llm', tags=['llm'])

secret = dotenv_values('.secret')


class SubscribeRequest(BaseModel):
    text: str
    chat_history: List[str]
    utterance_type: str


@router.post("/draft", status_code=200)
async def draft(r: SubscribeRequest):
    try:
        draft_module = Draft().activate_assertions()
        response = draft_module(r.text, r.chat_history, r.utterance_type)
        return {'llm': response}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=ex)


@router.post("/new", status_code=200)
async def new(r: SubscribeRequest):
    try:
        new_module = New().activate_assertions()
        response = new_module(r.text, r.chat_history, r.utterance_type)
        return {'llm': response}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=ex)


@router.post("/recording", status_code=200)
async def recording(r: SubscribeRequest):
    try:
        recording_module = Recording()
        response = recording_module(r.text, r.chat_history, r.utterance_type)
        return {'llm': response}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=ex)


@router.post("/evaluation", status_code=200)
async def evaluation(r: SubscribeRequest):
    try:
        evaluation_module = Evaluation()
        response = evaluation_module(r.msisdn, odoo_message)
        return {'llm': response}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=ex)
