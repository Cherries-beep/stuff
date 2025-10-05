""" Модуль с моделью """
import cv2
import numpy as np
import asyncio
import time
import math
from io import BytesIO
from tempfile import NamedTemporaryFile
import torch
from movinets import MoViNet
from movinets.config import _C

class MoViNetPipeline:
    """
    Обёртка над моделью MoViNet для обработки видео.
    1. Извлекает кадры из видео.
    2. Прогоняет их через модель.
    3. Возвращает предсказанный класс.
    """

    def __init__(self, weights_path: str, num_classes: int, device: str = "cpu"):
        self.device = torch.device(device)

        self.model = MoViNet(_C.MODEL.MoViNetA0, pretrained=False) # создание архитектуру модели

        self.model.classifier[3] = torch.nn.Conv3d( # замена последнего слоя под кол-во классов
            in_channels=2048,
            out_channels=num_classes,
            kernel_size=(1, 1, 1),
            bias=True,
        )
        state_dict = torch.load(weights_path, map_location=self.device) # загружаем веса
        self.model.load_state_dict(state_dict)

        self.model.eval().to(self.device) # режим инференса

        self.idx_to_label = { # cловарь индексов → человекочитаемая метка
            0: 'Жарить', 1: 'Лицо', 2: 'Лопата', 3: 'Пока', 4: 'Привет!',
            5: 'С', 6: 'большой', 7: 'меня', 8: 'положительный', 9: 'пять',
            10: 'рот', 11: 'свет', 12: 'сердце'
        }

    @staticmethod
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
        # сохранение BytesIO во временный файл (OpenCV не умеет читать BytesIO)
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

    def predict(self, video_file) -> int:
        """
        Делает предсказание класса по видео.
        :returns: индекс предсказанного класса.

            :param video_file: Видео из BytesIO
            :type video_file: BytesIO
            :returns: Индекс предсказанного класса
            :rtype: int
        """
        frames = self.extract_frames(video_file) # преобразовать видео в кадры
        frames_np = np.stack(frames) # сбор всех кадров в один numpy-массив
        frames_tensor = torch.from_numpy(frames_np).float() # перевод numpy → в torch.Tensor
        frames_tensor = frames_tensor.permute(3, 0, 1, 2).unsqueeze(0) # [B, C, T, H, W]

        with torch.no_grad(): # сделать предсказание
            preds = self.model(frames_tensor.to(self.device)) # [1, 13]
            pred_class = preds.argmax(dim=1).item() # выбор индекса максимальной вероятности

        return pred_class

    def predict_video(self, video_file: BytesIO) -> str:
        """
        Делает предсказание по видео и возвращает человекочитаемую метку.

        :param video_file: Видео в памяти.
        :type video_file: BytesIO
        """
        idx = self.predict(video_file)
        return self.idx_to_label.get(idx, "Неизвестный класс")