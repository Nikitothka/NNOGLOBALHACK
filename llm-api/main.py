from typing import Optional
from datetime import date as dt_date

from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from app.schemas.generation import GigaChatResponse, GigaChatRequest
from app.schemas.recognition_audio import RecognitionResponse, RecognitionMessage
from app.services.audio_service import AudioRecognition
from app.services.gigachat_service.gigachat_interact import GigaChatService
from app.services.summary.get_info_for_summary import get_messages, get_bmessages

app = FastAPI(
    title="GigaChat API",
    description="API для работы с GigaChat через внешний GigaChain",
    version="1.0.0"
)
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешенные домены
    allow_credentials=True,  # Если нужно разрешить креденциалы (например, куки)
    allow_methods=["*"],  # Разрешенные методы (например, ["GET", "POST"])
    allow_headers=["*"],  # Разрешенные заголовки
)


@app.post("/llm/api/generate")
async def generate_text(message: GigaChatRequest, llm_service: GigaChatService = Depends(GigaChatService)):
    try:
        response = llm_service.send_message(message.content)
        print(response)
        print(type(response))
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/llm/api/generate")
async def generate_text(message: GigaChatRequest, llm_service: GigaChatService = Depends(GigaChatService)):
    try:
        response = llm_service.send_message(message.content)
        print(response)
        print(type(response))
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/llm/api/recognize_audio", response_model=RecognitionResponse)
async def recognize_audio(message: RecognitionMessage):
    audio = message.audio
    audio_service = AudioRecognition()
    text = await audio_service.recognize_audio(audio)
    return RecognitionResponse(text=text)


@app.post("/llm/api/summarize_messages")
async def summarize_messages(
        group_name: Optional[str] = None,
        topic: Optional[str] = None,
        date: Optional[dt_date] = dt_date.today(),
        llm_service: GigaChatService = Depends(GigaChatService)
):
    try:
        # Получаем сообщения из обеих функций
        messages = get_messages(date=date, title=group_name, topic=topic)
        business_messages = get_bmessages(date=date, first_name=group_name)

        # Объединяем сообщения в один текст
        all_messages = " ".join(messages + business_messages)

        # Отправляем для создания сводки
        summary = llm_service.send_message_for_summury(all_messages)

        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))