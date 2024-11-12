from fastapi import APIRouter, HTTPException
import requests
from app.models.project_payload import ProjectsPayload
from settings import headers, main_url

project_router = APIRouter()

# Получить проекты
@project_router.get("/projects")
def get_projects():
    response = requests.get(main_url + 'projects', headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

# Создать проект
@project_router.post("/projects")
def create_project(payload: ProjectsPayload):
    payload = {
        "title": f"{payload.title}"
    }
    response = requests.post(main_url + 'projects', json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
