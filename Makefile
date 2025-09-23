.PHONY: run dev build docker-run format lint test

# локальный запуск через uvicorn
run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# билд Docker-образа
build:
	docker build -t fastapi-app .

# запуск контейнера
docker-run:
	docker run -d -p 8000:8000 --name fastapi-container fastapi-app

# автоформатирование кода (например, black + isort)
format:
	uv run black app
	uv run isort app

# линтеры (например, flake8)
lint:
	uv run flake8 app

# тесты (pytest)
test:
	uv run pytest -v