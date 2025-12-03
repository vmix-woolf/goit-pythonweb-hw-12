# Проєкт зі створення REST API для управління контактами.

## Technology stack
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- Alembic
- Pydantic v2
- Docker

## Installation and launch
Install dependencies:
```poetry install```

Launch PostgreSQL via Docker:
```docker compose up -d```

Apply Alembic migrations:
```alembic upgrade head```

Launch the server:
```uvicorn app.main:app --reload```

API available at:
http://127.0.0.1:8000

Swagger UI:
http://127.0.0.1:8000/docs

## API functionality
POST /contacts — create a contact

GET /contacts — list of contacts

GET /contacts/{id} — get a contact

PUT /contacts/{id} — update a contact

DELETE /contacts/{id} — delete a contact

GET /contacts/search — search by first name, last name, email

GET /contacts/birthdays — birthdays in the next 7 days

## Alembic
Create migration:
```alembic revision --autogenerate -m “message”```

Apply migrations:
```alembic upgrade head```


## Друга частина. Авторизація, аватар, rate limiting, Authentication & Authorization

У другій частині проєкту додано повноцінну роботу з користувачами:

- Реєстрація користувача (POST /auth/signup)
- Підтвердження email через токен (GET /auth/verify)
- Логін і видача JWT (POST /auth/login)
- Захист усіх операцій з контактами через get_current_user
- Користувач бачить тільки власні контакти
- Токен містить sub = email
- Маршрут /auth/me повертає поточного користувача
- Email verification
- Rate limiting
- Ендпоінт ```/auth/me``` обмежено: 5 запитів на хвилину
- Бібліотека: slowapi.

### Avatar upload (Cloudinary)
Реалізовано маршрут:
POST /users/avatar

Функціонал:
- прийом файлу (multipart/form-data)
- завантаження в Cloudinary
- отримання avatar_url
- збереження у БД
- повернення посилання клієнту

Використовуються змінні оточення:

```
CLOUDINARY_NAME
CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET
```
### CORS
Увімкнено CORS middleware для роботи з фронтендом.

Дозволено origin: *

(для навчального середовища).

### JWT авторизація
- Реєстрація, логін, email verify
- Доступ до контактів тільки свого користувача
- CRUD контактів з прив’язкою до user_id
- Завантаження аватарів у Cloudinary
- Rate limiting /auth/me
- Увімкнений CORS