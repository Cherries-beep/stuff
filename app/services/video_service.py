""" Модуль содержащий логку обработки чанков: сборка, передача в модель """
from fastapi import UploadFile
from app.storage.memory_storage import SessionManager


class VideoService:
    def __init__(self, session_manager: SessionManager) -> None:
        """
            Инициализация инстанса.
            :param session_manager: менеджер сессии
            :type session_manager: SessionManager
        """
        self.session_manager = session_manager

    async def handle_chunk(self,file: UploadFile, session_id: str, chunk_index: int, is_final: bool) -> str | None:
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
        assembled_file = await self.session_manager.save_chunk(file, session_id, is_final)

        if is_final and assembled_file is not None:
            final_text = "fake result"

            return final_text

        return None