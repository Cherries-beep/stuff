""" Модуль для работы с памятью """

from io import BytesIO

sessions = {} # словарь сессии

async def save_chunk_to_memory(file, session_id: str, chunk_index: int, is_final: bool):
    """ Сохранение чанка в ОЗУ (BytesIO) :
        - при первом чанке создается новый BytesIO
        - записывается содержимое чанка
        - если чанк финальные - возвращает BytesIO
    """

    if session_id not in sessions:
        sessions[session_id] = BytesIO()

    chunk_data = await file.read() # чтение чанка (байтов)
    sessions[session_id].write(chunk_data) # пишем в BytesIO

    if is_final:
        sessions[session_id].seek(0)
        return sessions[session_id]

    return None


# def assemble_file(session_id: str) -> BytesIO:
#     """ Получение файла из BytesIO """
#
#     if session_id not in sessions:
#         raise ValueError("Session not found")
#
#     buffer = sessions[session_id]
#     buffer.seek(0) # переместить курсор в начало буфера чтобы чтение началось с начала файла
#
#     return buffer



