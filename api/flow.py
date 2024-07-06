from fastapi import APIRouter, Request, BackgroundTasks, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder

import json
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1, hashes
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from rich import print
from dotenv import dotenv_values

from integration.odoo.tables import HrApplicant
from samantha.src.machinery import DataManager, ScoreWrapper


router = APIRouter(prefix='/flow', tags=['flow'])

secret = dotenv_values('.secret')
PASSPHRASE = secret['PASSPHRASE']


with open("api/.certs/private.pem", "rt") as file:
    PRIVATE_KEY = file.read()

    
@router.get("/", status_code=200)
async def entrypoint_(request: Request):
    try:
        data = await request.json()
        print(data)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    return jsonable_encoder({"status": "success"})


def register_db(partner_phone: str, partner_name: str, english_level: int) -> None:
    try:
        data = DataManager()
        appl = HrApplicant()
        appl.partner_phone = partner_phone
        appl.name = "Sales Agent"
        appl.partner_name = partner_name
        english_level = english_level
        data.applicant_register(appl, english_level=english_level)
    except Exception as ex:
        print(ex)


@router.post("/register", status_code=200)
async def register_(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()

        decrypted_data, aes_key, iv = decrypt_request(data)

        if decrypted_data['action'] == "ping":
            return ping_(decrypted_data['version'], aes_key, iv)
        
        if decrypted_data['action'] == "INIT":
            response =  {
                "version": decrypted_data['version'],
                "screen": "APPLICANT_BASIC",
                "data": { }
            }

        if decrypted_data['action'] == "data_exchange":
            print(decrypted_data)
            data = decrypted_data['data']
            partner_phone = data['msisdn']
            partner_name = f"{data['first_name']} {data['last_name']}"
            english_level = data['english_level']
            campaign = data['campaign']
            background_tasks.add_task(
                register_db,
                partner_phone=partner_phone,
                partner_name=partner_name,
                english_level=english_level
            )
            response =  {
                "version": decrypted_data['version'],
                "screen": "SUCCESS",
                "data": {
                    "extension_message_response": {
                        "params": decrypted_data['flow_token']
                    }
                 }
            }

        # Return the next screen & data to the client
        response = encrypt_response(response, aes_key, iv)
        return Response(content=response, media_type="text/plain")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    

def validate_grammar(text: str, msisdn: str, campaign: str):
    try:
      scorer = ScoreWrapper(msisdn, campaign)
      scorer.validate_grammar(text=text)
    except Exception as ex:
        print(ex)

@router.post("/assessment", status_code=200)
async def assessment_(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()

        decrypted_data, aes_key, iv = decrypt_request(data)

        if decrypted_data['action'] == "ping":
            return ping_(decrypted_data['version'], aes_key, iv)
           
        if decrypted_data['action'] == "INIT":
            response =  {
                "version": decrypted_data['version'],
                "screen": "APPLICANT_ASSESSMENT_ONE",
                "data": { }
            }

        if decrypted_data['action'] == "data_exchange":
            print(decrypted_data)
            # "payload": {
            #     "question_one": "${data.question_one}",
            #     "question_two": "${form.question_two}",
            #     "msisdn": "${screen.APPLICANT_ASSESSMENT_ONE.data.msisdn}",
            #     "campaign": "${screen.APPLICANT_ASSESSMENT_ONE.data.campaign}"
            # }
            data = decrypted_data['data']
            answers = f"{data['question_one']} ... {data['question_two']}"
            msisdn = data['msisdn']
            campaign = data['campaign']
            background_tasks.add_task(
                validate_grammar,
                text=answers,
                msisdn=msisdn,
                campaign=campaign
            )
            response =  {
                "version": decrypted_data['version'],
                "screen": "SUCCESS",
                "data": {
                    "extension_message_response": {
                        "params": decrypted_data['flow_token']
                    }
                 }
            }

        # Return the next screen & data to the client
        response = encrypt_response(response, aes_key, iv)
        return Response(content=response, media_type="text/plain")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


def decrypt_request(data: dict):
    # Read the request fields
    encrypted_flow_data_b64 = data['encrypted_flow_data']
    encrypted_aes_key_b64 = data['encrypted_aes_key']
    initial_vector_b64 = data['initial_vector']

    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    # password HERE
    private_key = load_pem_private_key(PRIVATE_KEY.encode('utf-8'), password=PASSPHRASE.encode('utf-8'))
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    encrypted_flow_data_tag = flow_data[-16:]
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    return decrypted_data, aes_key, iv


def encrypt_response(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")


def ping_(version: str, aes_key: str , iv: str) -> Response:
    response =  {
        "version": version,
        "data": { "status": "active" }
    }
    response = encrypt_response(response, aes_key, iv)
    return Response(content=response, media_type="text/plain")


@router.get("/dummy", status_code=200)
async def dummy_(request: Request):
    try:
        private_key = load_pem_private_key(PRIVATE_KEY.encode('utf-8'), password=PASSPHRASE.encode('utf-8'))
        print(private_key)
        return "See your terminal screen in vscode!"
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    

if __name__ == "__main__":
    private_key = load_pem_private_key(PRIVATE_KEY.encode('utf-8'), password=PASSPHRASE.encode('utf-8'))
    print(private_key)