#!/bin/sh

set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo " Waiting for Postgres Database Startup($POSTGRES_HOST $POSTGRES_PORT )..."
  sleep 0.1
 done

 echo "Postgres Database Started Successfully($POSTGRES_HOST:$POSTGRES_PORT)"

 python manage.py collectstatic --noinput
 python manage.py makemigrations --noinput
 python manage.py migrate --noinput
 python manage.py runserver 0.0.0.0:8000