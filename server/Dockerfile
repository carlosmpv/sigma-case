FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /app

RUN apt update && apt install -y gcc python3-dev libpq-dev

WORKDIR /app
RUN uv sync --frozen --no-cache

EXPOSE 8001
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8001"]