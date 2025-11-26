FROM python:3.13-slim AS builder
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NEW_RELIC_APP_NAME="pegasus-entrega4"
ENV NEW_RELIC_CONFIG_FILE="/app/newrelic.ini"

COPY . /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 5000
CMD ["newrelic-admin", "run-program", "gunicorn", "wsgi:application", "--log-file", "-", "--bind", "0.0.0.0:5000"]