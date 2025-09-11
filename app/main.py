""" Модуль для инициализации fastapi и подключения роутов """
from fastapi import FastAPI
from app.api.video_routes import router as video_router

app = FastAPI(title="App for speech recognition")

app.include_router(video_router)
