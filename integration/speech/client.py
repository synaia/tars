import time
import hashlib
import requests
import json
from pathlib import Path
from dotenv import dotenv_values

secret = dotenv_values('.secret')

SPEECHACE_API_KEY = secret['SPEECHACE_API_KEY']

SPEECH_SUPER_APP_ID = secret['SPEECH_SUPER_APP_ID']
SPEECH_SUPER_KEY = secret['SPEECH_SUPER_KEY']
SYNAIA_TOKEN_ID = secret['SYNAIA_TOKEN_ID']
API_URL = f"https://api.speechsuper.com/"



class SpeechSuperClient:
    PARAG_EVAL = "para.eval"
    SPEACK_EVAL_PRO = "speak.eval.pro"

    def __init__(self) -> None:
        self.headers = {}

    def request_scripted(self, audio_name: str, coreType: str, refText: str) -> dict:
        audioPath =  audio_name
        audioType = "wav" # Change the audio type corresponding to the audio file.
        audioSampleRate = 16000
        userId = "synaia"

        timestamp = str(int(time.time()))

        url =  API_URL + coreType
        connectStr = (SPEECH_SUPER_APP_ID + timestamp + SPEECH_SUPER_KEY).encode("utf-8")
        connectSig = hashlib.sha1(connectStr).hexdigest()
        startStr = (SPEECH_SUPER_APP_ID + timestamp + userId + SPEECH_SUPER_KEY).encode("utf-8")
        startSig = hashlib.sha1(startStr).hexdigest()

        params={
            "connect":{
                "cmd":"connect",
                "param":{
                    "sdk":{
                        "version": 16777472,
                        "source": 9,
                        "protocol": 2
                    },
                    "app":{
                        "applicationId":SPEECH_SUPER_APP_ID,
                        "sig":connectSig,
                        "timestamp":timestamp
                    }
                }
            },
            "start":{
                "cmd":"start",
                "param":{
                    "app":{
                        "userId": userId,
                        "applicationId": SPEECH_SUPER_APP_ID,
                        "timestamp": timestamp,
                        "sig": startSig
                    },
                    "audio":{
                        "audioType":audioType,
                        "channel":1,
                        "sampleBytes":2,
                        "sampleRate":audioSampleRate
                    },
                    "request":{
                        "coreType": coreType,
                        "refText": refText,
                        "tokenId": SYNAIA_TOKEN_ID,
                        "precision": 0.1,
                    }

                }
            }
        }

        datas=json.dumps(params)
        data={'text': datas}
        headers={"Request-Index": "0"}
        files={"audio": open(audioPath, 'rb')}
        res=requests.post(url, data=data, headers=headers, files=files)

        return res.json()
    

    def request_spontaneous_unscripted(self, audio_name: str, coreType: str, question_prompt: str, task_type: str) -> dict:
        audioPath =  audio_name
        audioType = "wav" # Change the audio type corresponding to the audio file.
        audioSampleRate = 16000
        userId = "synaia"

        timestamp = str(int(time.time()))

        url =  API_URL + coreType
        connectStr = (SPEECH_SUPER_APP_ID + timestamp + SPEECH_SUPER_KEY).encode("utf-8")
        connectSig = hashlib.sha1(connectStr).hexdigest()
        startStr = (SPEECH_SUPER_APP_ID + timestamp + userId + SPEECH_SUPER_KEY).encode("utf-8")
        startSig = hashlib.sha1(startStr).hexdigest()

        params={
            "connect":{
                "cmd":"connect",
                "param":{
                    "sdk":{
                        "version": 16777472,
                        "source": 9,
                        "protocol": 2
                    },
                    "app":{
                        "applicationId":SPEECH_SUPER_APP_ID,
                        "sig":connectSig,
                        "timestamp":timestamp
                    }
                }
            },
            "start":{
                "cmd":"start",
                "param":{
                    "app":{
                        "userId": userId,
                        "applicationId": SPEECH_SUPER_APP_ID,
                        "timestamp": timestamp,
                        "sig": startSig
                    },
                    "audio":{
                        "audioType":audioType,
                        "channel":1,
                        "sampleBytes":2,
                        "sampleRate":audioSampleRate
                    },
                   "request":{
                        "coreType":coreType,
                        "tokenId":"tokenId",
                        "precision": 0.1,
                        "question_prompt": question_prompt,
                        "test_type": "ielts",
                        "task_type": task_type, # ielts_part1, ielts_part2, ielts_part3
                        "phoneme_output": 0, # Return linking, loss of plosion and phoneme-level scores in the results
                        "model": "non_native",
                        "penalize_offtopic": 1, # To penalize irrelevant response   
                        "decimal_point": 1, 
                    }
                }
            }
        }

        datas=json.dumps(params)
        data={'text': datas}
        headers={"Request-Index": "0"}
        files={"audio": open(audioPath, 'rb')}
        res=requests.post(url, data=data, headers=headers, files=files)

        return res.json()



if __name__ == "__main__":
    # audio = "/Users/beltre.wilton/apps/preescrening_audios/waves/jirsed-b-C1.wav"
    # text = """
    #  In my previous role at a call center, I managed customer inquiries and resolved issues efficiently. I utilized active listening and problem-solving skills to enhance customer satisfaction. My ability to handle high-stress situations and maintain a professional demeanor contributed to a positive customer experience. This role honed my communication and multitasking abilities.
    # """
    # scores = SpeechSuperClient().request_scripted(audio_name=audio, coreType=SpeechSuperClient.PARAG_EVAL, refText=text)
    # print(scores)
    audio = "/Users/beltre.wilton/apps/preescrening_audios/unscripted/Hannah.wav"
    question = "Describe a film character played by an actor/actress whom you admire."
    scores = SpeechSuperClient().request_spontaneous_unscripted(
        audio_name=audio,
        coreType=SpeechSuperClient.SPEACK_EVAL_PRO,
        question_prompt=question
    )
    print(scores)



