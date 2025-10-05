""" Маршруты для работы с видео """
from fastapi import APIRouter, UploadFile, Form, HTTPException, status, Depends
from typing import Any
from uuid import UUID
from fastapi.responses import JSONResponse
from app.services.video_service import VideoService
from app.api.api_di import get_video_service

video_router = APIRouter()

@video_router.post('/api/upload-video', status_code=status.HTTP_201_CREATED)
async def upload_video(
        file: UploadFile,
        session_d: UUID = Form(..., alias='sessionId'),
        chunk_index: int = Form(..., alias='chunkIndex'),
        is_final: bool = Form(..., alias='isFinal'),
        service: VideoService = Depends(get_video_service)
) -> JSONResponse:
    """ Эндпоинт загрузки видео чанками

        :param file: Загружаемый файл чанка.
        :type file: UploadFile
        :param sessionId: Общий ID всей загрузки.
        :type sessionId: UUID
        :param chunkIndex: Индекс чанка.
        :type chunkIndex: int
        :param isFinal: Флаг, что это последний чанк.
        :type isFinal: bool
        :returns: JSON-ответ с финальным текстом или статусом загрузки.
        :rtype: dict[str, Any]
        """
    final_text = await service.handle_chunk(file, str(sessionId), chunkIndex, isFinal)

    return JSONResponse({"finalText": final_text})