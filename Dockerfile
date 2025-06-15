FROM python:3.11-slim

WORKDIR /app

COPY main.py ./
COPY env ./
COPY pyproject.toml ./
COPY README.md ./

# Установка зависимостей
RUN pip install --upgrade pip && \
    pip install python-dotenv && \
    pip install -r <(pipenv lock -r 2>/dev/null || echo '') || true && \
    pip install python-telegram-bot pytz

# Экспорт переменных окружения из файла env
RUN apt-get update && apt-get install -y dos2unix && dos2unix env

CMD ["python", "main.py"]
