#!/bin/sh
python3 manage.py migrate
python3 manage.py collectstatic
gunicorn --bind 0.0.0.0:8888 sara_server.asgi:application -k uvicorn.workers.UvicornWorker -w 2 &
nginx
