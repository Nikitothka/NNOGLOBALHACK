import requests
from fastapi import HTTPException

def make_request(method: str, url: str, headers: dict, json: dict = None):
    response = requests.request(method, url, headers=headers, json=json)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()