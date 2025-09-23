from fastapi import APIRouter, UploadFile, Form, HTTPException, status
from uuid import UUID
from app.services.video_service import handle_chunk
from typing import Any

router = APIRouter()

@router.post('/api/upload-video')
async def upload_video(
        file: UploadFile,
        sessionId: UUID = Form(...),
        chunkIndex: int = Form(...),
        isFinal: bool = Form(...)
) -> dict [str, Any]:
    """ Эндпоинт загрузки видео чанками

        Args:
            file: файл,
            sessionId: общий ID всей загрузки,
            chunkIndex: индекс чанка,
            isFinal: флаг последнего чанка.

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
    try:
        result = await handle_chunk(file, str(sessionId), chunkIndex, isFinal)

        if result is None: # промежуточный чанк
            return {"status": status.HTTP_201_CREATED}

        else: # финальный чанк
            return {'finalText': result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))