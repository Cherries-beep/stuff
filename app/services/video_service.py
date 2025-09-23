""" Модуль содержащий логку обработки чанков: сборка, передача в модель """
import asyncio
from fastapi import UploadFile
from app.storage.memory_storage import save_chunk_to_memory
from app.ml.pipeline import model

async def handle_chunk(file: UploadFile, session_id: str, chunk_index: int, is_final: bool) -> str | None:
    """ Обработка загруженного чанка:
        - сохраняет в память (BytesIO)
        - если промежуточный -> вернет None
        - если финальный - сборка видео и запуск Ml

        :param file: загружаемый файл
        :type file: UploadFile,
        :param session_id: общий id всей загрузки,
        :type session_id: str,
        :param chunk_index: Индекс чанка в последовательности.
        :type chunk_index: int
        :param is_final: Флаг, что это последний чанк.
        :type is_final: bool
        :returns: Финальный текст или None (для промежуточных чанков).
        :rtype: str | None
        """
    assembled_file = await save_chunk_to_memory(file, session_id, chunk_index, is_final) # готовый видеофайл в памяти)

    if not is_final: # промежуточный чанк
        return None

    final_text = await model.predict(assembled_file) # assembled_file — это BytesIO, теперь через DummySignModel

    return final_text
