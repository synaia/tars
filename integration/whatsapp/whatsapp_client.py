import os
import uuid
import subprocess
import requests
import json

from dotenv import dotenv_values

secret = dotenv_values('.secret')
AUDIO_RECORDING_PATH = secret["AUDIO_RECORDING_PATH"]
WHATSAPP_DEBUG = secret["WHATSAPP_DEBUG"]


class WhatsAppClient:
    API_URL = "https://graph.facebook.com/v20.0/"
    API_URL_ALONE = API_URL
    SYNAIA_META_USER_TOKEN = secret["SYNAIA_META_USER_TOKEN"]
    SYNAIA_META_NUMBER_ID = secret["SYNAIA_META_NUMBER_ID"]

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.SYNAIA_META_USER_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.SYNAIA_META_NUMBER_ID
        self.DEBUG = True if WHATSAPP_DEBUG == "True" else False
        print()

    def send_template_message(self, template_name, language_code, phone_number):
        if self.DEBUG:
            return
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }

        response = requests.post(
            f"{self.API_URL}/messages", json=payload, headers=self.headers)

        assert response.status_code == 200, "Error sending message"

        return response.status_code

    def send_text_message(self, message, phone_number):
        if self.DEBUG:
            return

        payload = {
            "messaging_product": 'whatsapp',
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        response = requests.post(
            f"{self.API_URL}/messages", json=payload, headers=self.headers)
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200, "Error sending message"
        return response.status_code
    
    def send_flow_basic(self,  phone_number: str, campaign: str):
        flow_id = secret['SYNAIA_FLOW_APPL_BASIC_ID']
        cta = "Please fill this form"
        screen = "APPLICANT_BASIC"
        return self.send_flow_(
            flow_id=flow_id,
            phone_number=phone_number,
            cta=cta,
            screen=screen,
            campaign=campaign
        )
    
    def send_flow_assessment(self,  phone_number: str, campaign: str):
        flow_id = secret['SYNAIA_FLOW_APPL_ASSESSMENT_ID']
        cta = "Please fill the assessment"
        screen = "APPLICANT_ASSESSMENT_ONE"
        return self.send_flow_(
            flow_id=flow_id,
            phone_number=phone_number,
            cta=cta,
            screen=screen,
            campaign=campaign
        )

    def send_flow_(self, flow_id: str, phone_number: str, cta: str, screen: str, campaign: str, header: str = "Flow message header", body: str = "Flow message body", footer: str = "Flow message footer", mode: str = "draft"):
        if self.DEBUG:
            return

        payload = {
            "recipient_type": "individual",
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "interactive",
            "interactive": {
                "type": "flow",
                "header": {
                    "type": "text",
                    "text": header
                },
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "name": "flow",
                    "parameters": {
                        "mode": mode,
                        "flow_message_version": "3",
                        "flow_token": str(uuid.uuid4()),
                        "flow_id": flow_id,
                        "flow_cta": cta,
                        "flow_action": "navigate",
                        "flow_action_payload": {
                            "screen": screen,
                            "data": {
                                "msisdn": phone_number,
                                "campaign": campaign
                            }
                        }
                    }
                }
            }
        }

        response = requests.post(
            f"{self.API_URL}/messages", json=payload, headers=self.headers)
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200, "Error sending message"
        return response.status_code

    def send_typing_on(self, phone_number):
        if self.DEBUG:
            return
        payload = {
            "messaging_product": 'whatsapp',
            "to": phone_number,
            "type": "TEXT",
            "typing": 'TYPING_ON'
        }
        response = requests.post(
            f"{self.API_URL}/messages", json=payload, headers=self.headers)
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200, "Error sending TYPING_ON"
        return response.status_code

    # TO REPLY ...
    # context: {
    #       message_id: message.id, // shows the message as a reply to the original user message
    #     },

    def wa_readed(self, wamid: str):
        if self.DEBUG:
            return
        payload = {
            "messaging_product": 'whatsapp',
            "status": "read",
            "message_id": wamid
        }
        response = requests.post(
            f"{self.API_URL}/messages", json=payload, headers=self.headers)
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200, "Error sending TYPING_ON"
        return response.status_code

    def convert_to_wav(self, ogg_file_name: str, step: int) -> None:
        wave_path = ogg_file_name.replace(".ogg", f"__step_{str(step)}.wav")
        command = [
            'ffmpeg',
            '-y',
            '-i', ogg_file_name,
            '-acodec', 'pcm_s16le',
            '-ac', '1',
            '-ar', '16000',
            wave_path
        ]
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if result.returncode != 0:
                raise RuntimeError(f"Error ffmpeg {result.stderr}")
            return wave_path
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")

    def process_audio(self, audio_id: str, msisdn: str, campaign: str, step: int):
        print(f"{self.API_URL_ALONE}{audio_id}")
        response = requests.get(
            f"{self.API_URL_ALONE}/{audio_id}", headers=self.headers, stream=True)
        wave_path = None
        if response.status_code == 200:
            body = json.loads(response.text)
            url = body['url']
            mediaresponse = requests.get(url, headers=self.headers)
            audio = f"{AUDIO_RECORDING_PATH}/{msisdn}-{campaign}.ogg"
            if mediaresponse.status_code == 200:
                with open(audio, "wb") as ogg:
                    for chunk in mediaresponse.iter_content(chunk_size=1024):
                        ogg.write(chunk)
                print(f'File {audio} downloaded successfully.')
                wave_path = self.convert_to_wav(audio, step)
            else:
                print(
                    f"Failed to download file. Status code: {mediaresponse.status_code}")
        return response.status_code, wave_path

    def process_notification(self, data):
        print(str(data))
        entries = data["entry"]
        for entry in entries:
            for change in entry["changes"]:
                value = change["value"]
                if value:
                    if "messages" in value:
                        for message in value["messages"]:
                            if message["type"] == "text":
                                from_no = message["from"]
                                id = message["id"]
                                message_body = message["text"]["body"]
                                prompt = message_body
                                print(
                                    f"Ack from FastAPI-WtsApp Webhook: {message_body}")
                                return {
                                    "statusCode": 200,
                                    "body": prompt,
                                    "from_no": from_no,
                                    "id": id,
                                    "isBase64Encoded": False,
                                    "type": "text",
                                    "flow": False
                                }
                            
                            if message["type"] == "audio":
                                from_no = message["from"]
                                id = message["id"]
                                audio_id = message['audio']['id']
                                return {
                                    "statusCode": 200,
                                    "audio_id": audio_id,
                                    "from_no": from_no,
                                    "id": id,
                                    "isBase64Encoded": False,
                                    "type": "audio"
                                }
                            
                            if message["type"] == "interactive":
                                from_no = message["from"]
                                id = message["id"]
                                interactive = message.get('interactive', None)
                                if interactive:
                                    nfm_reply = interactive.get('nfm_reply', None)
                                    if nfm_reply:
                                        if nfm_reply['name'] == "flow" and nfm_reply['body'] == "Sent":
                                            return {
                                                "statusCode": 200,
                                                "body": "Task completed",
                                                "from_no": from_no,
                                                "id": id,
                                                "isBase64Encoded": False,
                                                "type": "text",
                                                "flow": True
                                            }



        return {
            "statusCode": 403,
            "body": json.dumps("Unsupported method"),
            "isBase64Encoded": False
        }


if __name__ == "__main__":
    client = WhatsAppClient()
    # send a template message
    # client.process_audio(audio_id="8076039309081304", msisdn="18296456177", campaign="GET_FROM_SENDER")
    client.convert_to_wav(
        ogg_file_name="/Users/beltre.wilton/apps/preescrening_audios/18296456177-GET_FROM_SENDER.ogg")
