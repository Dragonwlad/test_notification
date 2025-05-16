# Stage 1: Builder
FROM python:3.13.3-bookworm AS builder

# Копируем uv из внешнего образа
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Рабочая директория
WORKDIR /app

# Установка зависимостей через uv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable --no-dev

# Копируем код проекта
ADD . /app

# Повторная синхронизация проекта
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable --no-dev

# Stage 2: Final
FROM python:3.13.3-bookworm

# Копируем uv в финальный образ
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Копируем окружение проекта
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app
# Рабочая директория
WORKDIR /app

# Используем виртуальное окружение по умолчанию
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONFAULTHANDLER=1

# Команда запуска приложения
CMD ["python3", "src/run_uvicorn.py"]
