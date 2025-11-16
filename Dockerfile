FROM python:3.13-slim AS builder
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 5000
CMD ["gunicorn","wsgi:applicantion","--log-file","-","--bind","0.0.0.0:5000"]