#!/bin/bash
source /home/ubuntu/startlens/venv/bin/activate
aws s3 cp s3://startlens-media-storage/config/.env?versionId=null /home/ubuntu/startlens/startlens_django/.env
python /home/ubuntu/startlens/startlens_django/manage.py collectstatic --noinput