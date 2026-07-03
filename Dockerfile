FROM python:3.13-slim
ARG TARGETARCH

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code
COPY pyproject.toml uv.lock /code/
RUN uv sync --locked --no-install-project
COPY . /code
RUN uv sync --locked

ENV PORT 8000
EXPOSE 8000

CMD ["uv", "run", "gunicorn", "app.main:app"]
