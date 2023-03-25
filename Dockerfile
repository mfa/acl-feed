FROM python:3.11

COPY app /app
COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

ENV PORT 8000
EXPOSE 8000
WORKDIR /

CMD ["gunicorn", "app.main:app"]
