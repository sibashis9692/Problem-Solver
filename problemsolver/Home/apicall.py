import requests
from dotenv import load_dotenv
import os
def data(code, language, input):
    load_dotenv()
    url = "https://online-code-compiler.p.rapidapi.com/v1/"

    payload = {
        "language": language,
        "version": "latest",
        "code": code,
        "input": input
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv('X_RapidAPI_Key'),
        "X-RapidAPI-Host": "online-code-compiler.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    return(response.json())
