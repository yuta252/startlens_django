#!/bin/bash
cd /home/ubuntu/startlens/startlens_django
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf