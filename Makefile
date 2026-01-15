.PHONY: install dev start build render-start

install:
	uv sync

lint:
	uv run ruff check .

# Локальная разработка (режим debug)
dev:
	uv run flask --debug --app src.page_analyzer:app run

# Запуск приложения с помощью Gunicorn (для продакшена)
start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

# Команда для деплоя на Render
render-start:
	gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app