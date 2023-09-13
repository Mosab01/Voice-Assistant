import os
import json
import urllib.request
import requests

import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()

def get_gpt_response(content):
    url = "https://open-ai21.p.rapidapi.com/conversationgpt35"

    data = {
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "stream": False
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST")
    }

    response = requests.post(url, json=data, headers=headers)
    res = response.json()
    gpt_response = res["BOT"]
    return gpt_response


def get_tts_response(text):
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv("XI_API_KEY"),
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    req = urllib.request.Request(
        url="https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM/stream",
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req) as res:
        with open("output.mp3", "wb") as f:
            f.write(res.read())
    
    print("Voice file downloaded successfully!")


def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        while True:
            audio = r.listen(source)

            try:
                recognized_text = r.recognize_google(audio)
                print("You said:", recognized_text)
                gpt_response = get_gpt_response(recognized_text)
                get_tts_response(gpt_response)
                break

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))


if __name__ == "__main__":
    main()