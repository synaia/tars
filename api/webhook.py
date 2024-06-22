from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from rich import print
from dotenv import dotenv_values
from samantha.src.machinery import SchedulerMachine
from integration.whatsapp.whatsapp_client import WhatsAppClient


router = APIRouter(prefix='/webhook', tags=['webhook'])

secret = dotenv_values('.secret')
    
    
@router.get("/")
def subscribe(request: Request):
    WHATSAPP_HOOK_TOKEN = request.app.state.secret['WHATSAPP_HOOK_TOKEN']
    print(WHATSAPP_HOOK_TOKEN)
    if request.query_params.get('hub.verify_token') == WHATSAPP_HOOK_TOKEN:
        return int(request.query_params.get('hub.challenge'))
    return "Authentication failed. Invalid Token."


def manage_message(msisdn: str, campaign: str, text: str, wamid: str, audio_id: str = None, message_type: str = "text"):
    wtsapp_client = WhatsAppClient()
    machine = SchedulerMachine(msisdn=msisdn, campaign=campaign,  wtsapp_client=wtsapp_client)
    if message_type == "audio":
        machine.manage_audio(audio_id)
    else:
        machine(text, wamid)


@router.post("/", status_code=200)
async def process_notifications(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    wtsapp_client = WhatsAppClient()
    print("We received ")
    print(data)
    response = wtsapp_client.process_notification(data)
    try:
        if response["statusCode"] == 200 and response["type"] == "text":
            if response["body"] and response["from_no"]:
                msisdn = response["from_no"]
                wamid = response["id"]
                campaign = "GET_FROM_SENDER"
                text = response['body']
                background_tasks.add_task(manage_message, msisdn=msisdn, campaign=campaign, text=text, wamid=wamid)
        if response["statusCode"] == 200 and response["type"] == "audio":
            msisdn = response["from_no"]
            wamid = response["id"]
            audio_id = response["audio_id"]
            campaign = "GET_FROM_SENDER"
            background_tasks.add_task(manage_message, msisdn=msisdn, campaign=campaign, text=None, wamid=wamid, audio_id=audio_id, message_type="audio")
    except Exception as ex:
        print(ex)
    return jsonable_encoder({"status": "success"})
