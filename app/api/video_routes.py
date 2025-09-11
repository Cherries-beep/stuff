from fastapi import APIRouter, UploadFile, Form, HTTPException, status
from uuid import UUID
from app.services.video_service import handle_chunk

router = APIRouter()

@router.post('/api/upload-video')
async def upload_video(
        file: UploadFile,
        sessionId: UUID = Form(...),
        chunkIndex: int = Form(...),
        isFinal: bool = Form(...)
):
    """ Эндпоинт загрузки видео чанками

        Args:
            file: файл
            sessionId: общий ID всей загрузки
            chunkIndex: индекс чанка
            isFinal: флаг последнего чанка.
    """

    try:
        result = await handle_chunk(file, str(sessionId), chunkIndex, isFinal)

        if result is None: # промежуточный чанк
            return {"status": status.HTTP_201_CREATED}

        else: # финальный чанк
            return {'finalText': result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))