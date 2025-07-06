FROM python:3.13
ARG TARGETARCH

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /code
WORKDIR /code
RUN uv sync --locked

ENV PORT 8000
EXPOSE 8000

CMD ["gunicorn", "app.main:app"]
