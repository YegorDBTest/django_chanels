#!/bin/bash

# while true; do
# 	sleep 60
# done

# python manage.py runserver 0:8000;

# daphne -b 0.0.0.0 -p 8000 main.asgi:application;

uvicorn --host=0.0.0.0 --port=8000 --workers=`nproc` main.asgi:application;
