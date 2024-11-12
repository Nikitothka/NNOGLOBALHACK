from fastapi import APIRouter, HTTPException
import requests
from app.models.boards_payload import BoardPayload
from settings import headers, main_url

boards_router = APIRouter()

# Получить проекты
@boards_router.get("/boards")
def get_boards():
    response = requests.get(main_url + 'boards', headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

# Создать проект
@boards_router.post("/boards")
def create_boards(payload: BoardPayload):
    payload = {
        "title": f"{payload.title}",
        "projectId": f"{payload.project_id}"
    }
    response = requests.request("POST", main_url + 'boards', json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
