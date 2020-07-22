#!/bin/bash
pkill -HUP gunicorn
cd /home/ubuntu/startlens/startlens_django
gunicorn --daemon --bind=0.0.0.0:8000 config.wsgi