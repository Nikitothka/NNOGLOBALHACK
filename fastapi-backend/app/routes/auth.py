from fastapi import APIRouter, HTTPException
import requests
from settings import main_url

from app.models.auth_payload import AuthPayload

auth_router = APIRouter()

@auth_router.post("/get_keys")
def get_keys(payload: AuthPayload):
    payload = {
        "login": f"{payload.login}",
        "password": f"{payload.password}"
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", main_url + 'auth/companies', json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    print(f"content {response.json()['content']}")
    ids = []
    for item in response.json()['content']:
        payload["companyId"] = item['id']

        response = requests.request("POST", main_url + 'auth/keys', json=payload, headers=headers)
        ids.append(response.json())

    return ids
