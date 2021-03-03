FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm -v /tmp/requirements.txt

COPY ./notpfdcm /app

ENV PORT=8000
EXPOSE ${PORT}
