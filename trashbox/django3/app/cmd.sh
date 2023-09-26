#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
  echo "Running Development Server"
  #python manage.py runserver_plus --cert-file ./server.crt
  python3 manage.py migrate
  python3 manage.py runserver 0.0.0.0:5000
  #python3 manage.py sslserver 0.0.0.0:5000 --certificate /app/ssl/foobar.crt --key /app/ssl/foobar.key
else
  echo "Running Production Server"
  python3 manage.py migrate
  #python manage.py runserver_plus --cert-file ./server.crt
  python3 manage.py runserver 0.0.0.0:5000
  #python3 manage.py sslserver 0.0.0.0:5000 --certificate /app/ssl/foobar.crt --key /app/ssl/foobar.key
fi



