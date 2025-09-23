""" Модуль для работы с памятью """
from io import BytesIO
from fastapi import UploadFile
from typing import Optional
from app.ml.pipeline import model

class SessionManager:
    """
    Менеджер сессий для хранения видео-чанков в памяти.
    Используется singleton, чтобы все сессии были глобальными
    """

    _instance: Optional["SessionManager"] = None
    sessions: dict[str, BytesIO]

    def __new__(cls) -> "SessionManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.sessions = {}
        return cls._instance

    def get_session(self, session_id: str) -> BytesIO:
        """
        Возвращает объект BytesIO для конкретной сессии. Если сессия не существует — создаёт новую.

        :param session_id: Идентификатор сессии.
        :type session_id: str
        :returns: BytesIO объект для сессии.
        :rtype: BytesIO
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = BytesIO()
        return self.sessions[session_id]

    async def save_chunk(
        self,
        file: UploadFile,
        session_id: str,
        is_final: bool
    ) -> Optional[BytesIO]:
        """
        Сохранение чанка в ОЗУ (BytesIO) :
        - при первом чанке создается новый BytesIO
        - записывается содержимое чанка
        - если чанк финальные - возвращает BytesIO

        :param file: Загружаемый файл чанка.
        :type file: UploadFile
        :param session_id: Общий ID всей загрузки.
        :type session_id: str
        :param is_final: Флаг, что это последний чанк.
        :type is_final: bool
        :returns: BytesIO, если финальный чанк, иначе None.
        :rtype: Optional[BytesIO]
        """
        session: BytesIO = self.get_session(session_id)
        chunk_data: bytes = await file.read()
        session.write(chunk_data)

        if is_final:
            session.seek(0)
            return session
        return None


session_manager: SessionManager = SessionManager() # глобальный менеджер сессий

async def handle_chunk(file: UploadFile, session_id: str, chunk_index: int,is_final: bool) -> Optional[str]:
    """
    Обрабатывает загруженный чанк:
    - сохраняет в память (BytesIO),
    - если промежуточный -> возвращает None,
    - если финальный -> собирает видео и запускает ML-модель.

    :param file: Загружаемый файл чанка.
    :type file: UploadFile
    :param session_id: Общий ID всей загрузки.
    :type session_id: str
    :param chunk_index: Индекс чанка.
    :type chunk_index: int
    :param is_final: Флаг, что это последний чанк.
    :type is_final: bool
    :returns: Результат работы модели, если финальный чанк, иначе None.
    :rtype: Optional[str]
    """
    assembled_file: Optional[BytesIO] = await session_manager.save_chunk(file, session_id, is_final)

    if not is_final:
        return None

    final_text: str = await model.predict(assembled_file) # здесь предполагаем вызов ML-модели
    return final_text