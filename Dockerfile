# образ на основе которого создаем контейнер
FROM python:3.11-slim

# рабочая директория
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# системные зависимости для git и OpenCV / видео
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# установка зависимостей, установка uv
COPY pyproject.toml uv.lock ./
RUN pip install --upgrade pip && pip install uv && uv sync --frozen

# копирование всего проекта
COPY . .

# запуск uvicorn (пока нет docker compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]