from fastapi import APIRouter, HTTPException
import requests
from settings import headers, main_url
from app.models.invite_payload import InvitePayload

user_router = APIRouter()

@user_router.get("/users")
def create_user():

    response = requests.request("GET", main_url + 'users', headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@user_router.post("/users")
def get_users(payload: InvitePayload):
    payload = {
        "email": f"{payload.email}",
        "isAdmin": False
    }

    response = requests.request("POST", main_url + 'users', headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@user_router.post("/users")
def invite_user(payload: InvitePayload):
    payload = {
        "email": f"{payload.email}",
        "isAdmin": False
    }

    response = requests.request("POST", main_url + 'users', headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
