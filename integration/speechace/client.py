import requests
from dotenv import dotenv_values
secret = dotenv_values('.secret')

SPEECHACE_API_KEY = secret['SPEECHACE_API_KEY']
AUDIO_RECORDING_PATH = secret['AUDIO_RECORDING_PATH']


class SpeechaceClient:
    API_URL = f"https://api.speechace.co/api/scoring/text/v9/json?key={SPEECHACE_API_KEY}&dialect=en-us"

    def __init__(self) -> None:
        self.headers = {
            "Content-Type": "application/json",
        }

    def request(self, text: str, audio: str, question_info: str = '\'u1/q3\'') -> dict:
        payload={
            'text': text,
            'question_info': question_info,
            'no_mc': '1' #Optional flag to indicate the text field contains multiple lines.
        }
        files=[
            ('user_audio_file',
                (audio, open(f"{AUDIO_RECORDING_PATH}/{audio}",'rb'),'audio/wav')
            )
        ]
        response = requests.request("POST", self.API_URL, headers=self.headers, data=payload, files=files)
        scores = response.json()
        return scores



# 'u1/q1'

# A unique identifier for the activity or question this user audio is answering.

# Structure this field to include as much info as possible to aid in reporting and analytics.

# For example: question_info='u1/q1' where:

# u1: means the question belongs to Unit 1 in your content
# q1: means this is question 1 within the unit
# You can add more levels as needed.

# Ensure no personally identifiable information is passed in this field.


