from fastapi import FastAPI
from app.api.video_routes import router as video_router

def create_app() -> FastAPI:
    """Создаёт и возвращает объект FastAPI с подключёнными роутами."""
    app = FastAPI(title="App for speech recognition")

    # подключаем роуты
    app.include_router(video_router)

    return app
