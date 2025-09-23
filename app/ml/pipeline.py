""" Модуль с мл моделью """

import cv2
import numpy as np
import asyncio
import time
import math
from io import BytesIO
from tempfile import NamedTemporaryFile


def busy_work(ms=500) -> float:
    """ Имитация загрузки CPU (как будто обрабатываем видео) """
    end = time.perf_counter() + ms / 1000
    x = 0
    while time.perf_counter() < end:
        x += math.sqrt(12345.6789)
    return x


class DummySignModel:

    def __init__(self, delay_ms: int = 1000):
        """
        Инициализация модели.

            :param delay_ms: Задержка обработки в миллисекундах.
            :type delay_ms: int
        """
        self.delay_ms = delay_ms
        self._lock = asyncio.Lock() # блокировка, чтобы не запускать параллельно

    async def predict(self, video_path: str) -> str:
        """
        Имитация асинхронной обработки видео:
        - ждём self.delay_ms (CPU-загрузка в отдельном потоке),
        - возвращаем фейковый текст

        :param video_path: Путь к видеофайлу.
        :type video_path: str
        :returns: Фейковый текст распознавания.
        :rtype: str
        """
        async with self._lock:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, busy_work, self.delay_ms)
            return f"Заглушка: распознанный текст из {video_path}"

model = DummySignModel(delay_ms=1500)

def process_video(video_file: BytesIO) -> str:
    """ Заглушка ML обработки видео: имитируем задержку (будто модель работает)

        :param video_file: Видео в памяти.
        :type video_file: BytesIO
        :returns: Фейковый текстовый результат распознавания.
        :rtype: str
    """
    time.sleep(2)

    return "Это фейковый перевод с видео. Временно"

def extract_frames(video_file: BytesIO) -> list[np.ndarray]:
    """
    - Сохраняет BytesIO во временный mp4,
    - Извлекает кадры через OpenCV (cv2.VideoCapture),
    - Делает каждый кадр resize 320х320,
    - Перевод кадра из BGR -> RGB,
    - Возвращает список numpy-массивов для модели

    :param video_file: Видео в памяти.
    :type video_file: BytesIO
    :returns: Список кадров в формате numpy-массивов (RGB, 320x320).
    :rtype: list[np.ndarray]
    """
    # сохранение BytesIO во временный файл (OpenCV не умеет читать BytesIO
    with NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(video_file.read())
        tmp_path = tmp.name

    cap = cv2.VideoCapture(tmp_path) # открытие видеофайла для покадрового чтения.
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (320, 320)) # приведение в 320х320
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # из BGR -> RGB
        frames.append(frame)

    cap.release()

    return frames


