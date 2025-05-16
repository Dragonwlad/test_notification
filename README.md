# Notifications API

Асинхронное API на FastAPI для управления уведомлениями пользователей. Поддерживает JWT-аутентификацию, регистрацию, пагинацию и защиту маршрутов.

## 🚀 Как запустить

1. Создай `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

2. Запусти проект через Docker Compose:

```bash
docker-compose up --build
```

API будет доступно по адресу:
`http://0.0.0.0:8000/api/`

---

## 🚀 Как запустить для локальной разработки

```bash
make postgres

make create_db

make run_uvicorn
```

API будет доступно по адресу:
`http://0.0.0.0:8000/api/`

---

## 📚 Документация

Интерактивная Swagger-документация доступна по адресу:
👉 [http://0.0.0.0:8000/docs#/](http://0.0.0.0:8000/docs#/)

---

## 🔀 Эндпоинты

### `/auth/register` \[POST]

Зарегистрировать нового пользователя.

**Request:**

```json
{
  "username": "yourname",
  "password": "yourpassword"
}
```

**Response:**

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

---

### `/auth/login` \[POST]

Войти и получить токены. Использует OAuth2-form `username/password`.

---

### `/auth/refresh` \[POST]

Обновить `access_token` с использованием `refresh_token`.

---

## 🔔 Уведомления

### `/notifications/` \[POST]

Создать уведомление (**только для авторизованных**).

**Request:**

```json
{
  "type": "like",
  "text": "You got a new like!"
}
```

---

### `/notifications/` \[GET]

Получить список уведомлений с пагинацией (**только для авторизованных**).

**Query-параметры:**

* `page`: номер страницы (default: 1)
* `per_page`: элементов на странице (default: 50)
* `order`: `asc` | `desc`

**Response:**

```json
{
  "total": 122,
  "count": 50,
  "page": 1,
  "pages": 3,
  "items": [
    {
      "id": 1,
      "type": "comment",
      "text": "new reply",
      "created_at": "...",
      "user_id": 5
    }
  ]
}
```

---

### `/notifications/{notification_id}` \[DELETE]

Удалить уведомление юзера (**только для авторизованных**).

---

## 📁 Структура

* `api/` — роуты
* `services/` — бизнес-логика
* `db/` — модели Tortoise ORM
* `rest_models/` — схемы ответа
* `settings.py` — конфигурация проекта

---

## 🚚 Зависимости

* **FastAPI** — фреймворк
* **Tortoise ORM** — асинхронная ORM
* **PyJWT** — работа с JWT
* **Pydantic** — схемы валидации
* **Docker** + **docker-compose** — деплой

---
