import requests
from pathlib import Path
from dotenv import dotenv_values
secret = dotenv_values('.secret')

SPEECHACE_API_KEY = secret['SPEECHACE_API_KEY']


class SpeechaceClient:
    API_URL = f"https://api.speechace.co/api/scoring/text/v9/json?key={SPEECHACE_API_KEY}&dialect=en-us"

    def __init__(self) -> None:
        self.headers = {}

    def request(self, text: str, audio: str, question_info: str = '\'u1/q1\'') -> dict:
        payload={
            'text': text,
            'question_info': question_info,
            'no_mc': '1' #Optional flag to indicate the text field contains multiple lines.
        }
        files=[
            ('user_audio_file',
                (Path(audio).name, open(audio,'rb'),'audio/wav')
            )
        ]
        response = requests.request("POST", self.API_URL, headers=self.headers, data=payload, files=files)
        scores = response.json()
        return scores


if __name__ == "__main__":
    audio = "/Users/beltre.wilton/apps/preescrening_audios/15_segs.wav"
    text = """
     If someone is upset on WhatsApp, you can be kind and listen to them. You can say sorry and try to help them feel better. 
     Maybe you can ask what they need and find a way to fix the problem. 
    """
    scores = SpeechaceClient().request(text=text, audio=audio)
    print(scores)

# 'u1/q1'

# A unique identifier for the activity or question this user audio is answering.

# Structure this field to include as much info as possible to aid in reporting and analytics.

# For example: question_info='u1/q1' where:

# u1: means the question belongs to Unit 1 in your content
# q1: means this is question 1 within the unit
# You can add more levels as needed.

# Ensure no personally identifiable information is passed in this field.


