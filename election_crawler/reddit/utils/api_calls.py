import requests
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('HATESPEECH_KEY')

URL = 'https://api.moderatehatespeech.com/api/v1/moderate/'
THRESHOLD = .85

def getToxic(body):   
    data={
        "token": KEY,
        "text": body
    }
    headers={
            "Content-Type": "application/json",
        }

    try:
        request = requests.post(
            URL,
            json=data
        ).json()
    except:
        print("got exception when pinging ModerateHatespeech")
        return -1

    try:
        if request["response"] != "Success":
            print("unsuccessful request w/ error: " + request["response"])
            toxic = -1

        elif request["class"] == "flag" and float(request["confidence"]) >= THRESHOLD:
            toxic = 1
        
        else: toxic = 0
    except:
        print("got exception after getting a response")
        return -1

    return toxic