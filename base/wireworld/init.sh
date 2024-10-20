#!/bin/sh

nginx -g 'daemon off;' &
uvicorn app.main:app --port 8000
