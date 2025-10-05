""" Модуль для работы с памятью """
from io import BytesIO
from fastapi import UploadFile

class SessionManager:
    """
    Менеджер сессий для хранения видео-чанков в памяти.
    Используется singleton, чтобы все сессии были глобальными
    """

    _instance: "SessionManager" | None = None
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

    async def save_chunk(self, file: UploadFile, session_id: str, is_final: bool) -> BytesIO | None:
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