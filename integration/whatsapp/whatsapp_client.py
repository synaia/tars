import os
import subprocess
import requests
import json

from dotenv import dotenv_values

secret = dotenv_values('.secret')
AUDIO_RECORDING_PATH = secret["AUDIO_RECORDING_PATH"]

class WhatsAppClient:
    API_URL = "https://graph.facebook.com/v19.0/"
    API_URL_ALONE = API_URL
    WHATSAPP_API_TOKEN = secret["WHATSAPP_API_TOKEN"]
    WHATSAPP_CLOUD_NUMBER_ID = secret["WHATSAPP_CLOUD_NUMBER_ID"]

    def __init__(self, debug: bool = False):
        self.headers = {
            "Authorization": f"Bearer {self.WHATSAPP_API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = self.API_URL + self.WHATSAPP_CLOUD_NUMBER_ID
        self.DEBUG = debug

    def send_template_message(self, template_name, language_code, phone_number):
        if self.DEBUG: return
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

        response = requests.post(f"{self.API_URL}/messages", json=payload,headers=self.headers)

        assert response.status_code == 200, "Error sending message"

        return response.status_code


    def send_text_message(self, message, phone_number):
        if self.DEBUG: return
        payload = {
            "messaging_product": 'whatsapp',
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        response = requests.post(f"{self.API_URL}/messages", json=payload, headers=self.headers)
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200, "Error sending message"
        return response.status_code
    

    def send_typing_on(self, phone_number):
        if self.DEBUG: return
        payload = {
            "messaging_product": 'whatsapp',
            "to": phone_number,
            "type": "TEXT",
            "typing": 'TYPING_ON'
        }
        response = requests.post(f"{self.API_URL}/messages", json=payload, headers=self.headers)
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200, "Error sending TYPING_ON"
        return response.status_code
    
    # TO REPLY ...
    # context: {
    #       message_id: message.id, // shows the message as a reply to the original user message
    #     },

    def wa_readed(self, wamid: str):
        if self.DEBUG: return
        payload = {
            "messaging_product": 'whatsapp',
            "status": "read",
            "message_id": wamid
        }
        response = requests.post(f"{self.API_URL}/messages", json=payload, headers=self.headers)
        print(response.status_code)
        print(response.text)
        assert response.status_code == 200, "Error sending TYPING_ON"
        return response.status_code
    
    
    def convert_to_wav(self, ogg_file_name: str) -> None:
        command = [
            'ffmpeg',
            '-y',
            '-i', ogg_file_name,
            '-acodec', 'pcm_s16le',
            '-ac', '1',
            '-ar', '16000',
            ogg_file_name.replace(".ogg", ".wav")
        ]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if result.returncode != 0:
                raise RuntimeError(f"Error ffmpeg {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
    

    def process_audio(self, audio_id: str, msisdn: str, campaign: str):
        print(f"{self.API_URL_ALONE}{audio_id}")
        response = requests.get(f"{self.API_URL_ALONE}/{audio_id}", headers=self.headers, stream=True)
        if response.status_code == 200:
            body = json.loads(response.text)
            url =body['url']
            mediaresponse = requests.get(url, headers=self.headers)
            audio = ""
            if mediaresponse.status_code == 200:
                audio = f"{AUDIO_RECORDING_PATH}/{msisdn}-{campaign}.ogg"
                with open(audio, "wb") as ogg:
                    for chunk in mediaresponse.iter_content(chunk_size=1024):
                        ogg.write(chunk)
                print(f'File {audio} downloaded successfully.')
                self.convert_to_wav(audio)
            else:
                print(f"Failed to download file. Status code: {mediaresponse.status_code}")
        return response.status_code, audio


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
                                print(f"Ack from FastAPI-WtsApp Webhook: {message_body}")
                                return {
                                    "statusCode": 200,
                                    "body": prompt,
                                    "from_no": from_no,
                                    "id": id,
                                    "isBase64Encoded": False,
                                    "type": "text"
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

        return {
            "statusCode": 403,
            "body": json.dumps("Unsupported method"),
            "isBase64Encoded": False
        }



if __name__ == "__main__":
    client = WhatsAppClient(debug=True)
    # send a template message
    # client.process_audio(audio_id="8076039309081304", msisdn="18296456177", campaign="GET_FROM_SENDER")
    client.convert_to_wav(ogg_file_name="/Users/beltre.wilton/apps/preescrening_audios/18296456177-GET_FROM_SENDER.ogg")
    
    