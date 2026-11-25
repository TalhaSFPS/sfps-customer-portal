#!/bin/sh
set -eu
python app.py
exec gunicorn --workers 2 --bind 0.0.0.0:$PORT app:app
