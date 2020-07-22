#!/bin/bash
source /home/ubuntu/startlens/venv/bin/activate
aws s3 cp s3://startlens-media-storage/config/.env /home/ubuntu/startlens/startlens_django/.env
python manage.py collectstatic --noinput