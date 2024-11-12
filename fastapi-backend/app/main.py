import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, users, projects, tasks, columns, chat, voice
from app.routes.bot_handler import bot_router
from contextlib import asynccontextmanager

from settings import userbot

@asynccontextmanager
async def lifespan(app: FastAPI):
    await userbot.start()
    logging.info("Userbot started.")
    yield
    await userbot.stop()
    logging.info("Userbot stopped.")

app = FastAPI(prefix="/api",
              docs_url="/yougile/api/api-docs",
              redoc_url="/yougile/api/redoc",
              openapi_url="/yougile/api/openapi.json",
              lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешенные домены
    allow_credentials=True,  # Если нужно разрешить креденциалы (например, куки)
    allow_methods=["*"],  # Разрешенные методы (например, ["GET", "POST"])
    allow_headers=["*"],  # Разрешенные заголовки
)
app.include_router(auth.auth_router, prefix="/yougile/api", tags=["Auth"])
app.include_router(users.user_router, prefix="/yougile/api", tags=["Users"])
app.include_router(projects.project_router,prefix="/yougile/api", tags=["Projects"])
app.include_router(tasks.task_router,prefix="/yougile/api", tags=["Tasks"])
app.include_router(columns.columns_router,prefix="/yougile/api", tags=["Columns"])
app.include_router(chat.chat_router,prefix="/yougile/api", tags=["Chat"])
# app.include_router(voice.voice_router,prefix="/yougile/api", tags=["Voice"])
app.include_router(bot_router,prefix="/yougile/api", tags=["Agnia"])

@app.get('/')
async def root():
    return {"message": "Hello!"}
