FROM python:3.12-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли залежностей
COPY pyproject.toml poetry.lock ./

# Встановлюємо Poetry
RUN pip install poetry

# Налаштовуємо Poetry
RUN poetry config virtualenvs.create false

# Встановлюємо залежності (БЕЗ dev залежностей)
RUN poetry install --only=main

# Копіюємо код застосунку
COPY . .

# Відкриваємо порт
EXPOSE 8000

# Команда запуску
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]