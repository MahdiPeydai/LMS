#!/bin/sh

while ! nc -z mysql 3306; do
  echo "Waiting for MySQL to start..."
  sleep 1
done

while ! nc -z redis 6379; do
  echo "Waiting for Redis to start..."
  sleep 1
done

exec gunicorn OnlineLearning.wsgi:application --bind 0.0.0.0:8000