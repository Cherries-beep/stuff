""" Модуль содержащий логку обработки чанков: сборка, передача в модель """
from fastapi import UploadFile
from app.storage.memory_storage import SessionManager
from app.ml.pipeline import MoViNetPipeline
from io import BytesIO


class VideoService:
    def __init__(self, session_manager: SessionManager, model_pipeline: MoViNetPipeline) -> None:
        """
            Инициализация инстанса.
            :param session_manager: менеджер сессии
            :type session_manager: SessionManager
        """
        self.session_manager = session_manager
        self.model_pipeline = model_pipeline

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
        assembled_file = await self.session_manager.save_chunk(file=file, session_id=session_id, is_final=is_final)

        if is_final and assembled_file is not None:
            final_text = self.predict_video(assembled_file) # прогон собранное видео через пайплайн модели
            return final_text

        return None

    def predict_video(self, video_file: BytesIO) -> str:
        """
        Прогоняет видео через модель и возвращает человекочитаемую метку жеста.

        :param video_file: видео в BytesIO
        :return: предсказанный жест в виде строки
        """
        # Используем пайплайн MoViNet
        return self.model_pipeline.predict_video(video_file)