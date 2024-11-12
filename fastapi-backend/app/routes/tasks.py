from datetime import datetime

from fastapi import APIRouter, HTTPException
import requests
from settings import headers, main_url
from app.models.tasks_payload import TaskPayload
from app.models.change_task_payload import CTaskPayload
from app.models.delete_payload import DeletePayload
from fastapi.responses import JSONResponse
import re
from app.utils.name_detector import get_column_id_by_name, get_user_id_by_name, get_task_id_by_name

task_router = APIRouter()

def get_deadline(timestamp):
    dt = datetime.fromtimestamp(timestamp / 1000)
    return f'2024-{dt.month}-{dt.day}'

@task_router.get("/tasks/{column_id}")
def get_tasks(column_id):
    params = {
        "columnId": column_id,
    }
    response = requests.get(main_url + f'tasks', headers=headers, params=params)

    answer = [
        {"title": i['title'],
         "column_id": i['columnId'],
         "task_id": i['id'],
         "deadline": get_deadline(i['deadline']['deadline']) if 'deadline' in i else None,
         "priority": "low",
         "description": re.sub(r'<[^>]+>', '', i['description']) if 'description' in i else None}
        for i in response.json()['content']
    ]
    print(answer)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    # return response.json()
    return JSONResponse(content=answer, status_code=200)

@task_router.post("/tasks")
def create_task(payload: TaskPayload):
    if payload.assigned is not None:
        assigned = [get_user_id_by_name(i) for i in payload.assigned]
    else:
        assigned = []
    params = {
        "title": payload.title,
        "columnId": "c9d7e268-78dc-4557-b096-2e92883c5227",
        "description": payload.description,
        "archived": False,
        "completed": False,
        "assigned": assigned
    }
    if payload.deadline is not None:
        params['deadline'] = {"deadline": payload.deadline}

    response = requests.post(main_url + f'tasks', headers=headers, json=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@task_router.put("/change_task")
def create_task(payload: CTaskPayload):
    print(payload)
    params = {
        "columnId": "-",
    }

    task_id = get_task_id_by_name(payload.task_id)
    requests.put(main_url + f'tasks/{task_id}', headers=headers, json=params)
    assigned = [get_user_id_by_name(i) for i in payload.assigned]
    if payload.column_id is None:
        params = {
            "title": payload.title,
            "columnId": "c9d7e268-78dc-4557-b096-2e92883c5227",
            "description": payload.description,
            "assigned": assigned,
        }
    else:
        column_id = get_column_id_by_name(payload.column_id)

        params = {
            "title": payload.title,
            "columnId": column_id,
            "description": payload.description,
            "assigned": assigned,
        }

    print(params)
    response = requests.post(main_url + f'tasks', headers=headers, json=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@task_router.put("/delete_task")
def create_task(payload: DeletePayload):
    print(payload)
    params = {
        "columnId": "-",
    }

    task_id = get_task_id_by_name(payload.title)
    response = requests.put(main_url + f'tasks/{task_id}', headers=headers, json=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
