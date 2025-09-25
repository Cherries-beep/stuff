from fastapi import FastAPI
from app.api import api_router

def create_app() -> FastAPI:
    """Создаёт и возвращает объект FastAPI с подключёнными роутами."""
    app = FastAPI(title="App for speech recognition")
    app.include_router(api_router)

    return app