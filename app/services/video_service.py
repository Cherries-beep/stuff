""" Модуль содержащий логку обработки чанков: сборка, передача в модель """

import asyncio

from fastapi import UploadFile
from app.storage.memory_storage import save_chunk_to_memory
from app.ml.pipeline import model

async def handle_chunk(file: UploadFile, session_id: str, chunk_index: int, is_final: bool):
    """ Обработка загруженного чанка:
        - сохраняет в память (BytesIO)
        - если промежуточный -> вернет None
        - если финальный - сборка видео и запуск Ml
    """
    assembled_file = await save_chunk_to_memory(file, session_id, chunk_index, is_final) # готовый видеофайл в памяти)

    if not is_final: # промежуточный чанк
        return None

    final_text = await model.predict(assembled_file) # assembled_file — это BytesIO, теперь через DummySignModel

    return final_text
