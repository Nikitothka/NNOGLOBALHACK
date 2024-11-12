from fastapi import APIRouter, HTTPException
import requests
from settings import headers, main_url
from app.models.columns_payload import ColumnPayload
from fastapi.responses import JSONResponse

columns_router = APIRouter()

@columns_router.get("/columns")
def get_columns():
    params = {"board_id": "346ad00e-097a-4ea1-87da-9ecb52f9a9e6"}
    response = requests.get(main_url + 'columns', headers=headers, json=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    colors = {"1": "#7B869E", "2": "#FF8C8C", "3": "#E9A24F", "4": "#FCE258", "5": "#7CAE5E", "6": "#49C5BC",
              "7": "#8CACFF", "8": "#CC8CFF", "9": "#667085", "10": "#EB3737",
              "11": "#F2732B", "12": "#F5CC00", "13": "#5CDC11", "14": "#08A7A9", "15": "#5089F2", "16": "#E25EF2"}
    answer = [
        {"title": i['title'],
         "color": colors[str(i['color'])],
         "column_id": i['id']} for i in response.json()['content']
    ]

    return JSONResponse(content=answer, status_code=200)

@columns_router.post("/columns")
def create_column(payload: ColumnPayload):
    params = {"title": f"{payload.title}",
              "boardId": f"{payload.board_id}"}
    response = requests.get(main_url + 'columns', headers=headers, json=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
