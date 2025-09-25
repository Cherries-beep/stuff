from fastapi import APIRouter
from app.api.video_router import video_router

api_router = APIRouter()
api_router.include_router(video_router, tags=["video"])
