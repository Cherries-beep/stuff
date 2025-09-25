""" Модуль для конфигурации зависимостей API для создания сервисов, которые будут
внедряться в роутеры через механизм dependency injection
"""
from app.services.video_service import VideoService
from app.storage.memory_storage import SessionManager

def get_session_manager() -> SessionManager:
    """Фабрика для SessionManager
        :returns: экземпляр SessionManager
        :rtype: SessionManager
    """
    return SessionManager()

def get_video_service() -> VideoService:
    """Фабрика для VideoService с инжектированным SessionManager
        :returns: экземпляр VideoService
        :rtype: VideoService
    """
    return VideoService(session_manager=get_session_manager())

