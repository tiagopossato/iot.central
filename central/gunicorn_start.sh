#!/bin/bash

NAME="central"                              #Name of the application (*)  
DJANGODIR=/opt/iot.central/central             # Django project directory (*)  
USER=central                                       # the user to run as (*)  
GROUP=nogroup                                     # the group to run as (*)  
NUM_WORKERS=2                                     # how many worker processes should Gunicorn spawn (*)  
TIMEOUT=120
DJANGO_SETTINGS_MODULE=central.settings             # which settings file should Django use (*)  
DJANGO_WSGI_MODULE=central.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR  
source /etc/profile

workon centralvenv
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE  
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# echo '---------------'
# echo
# echo 'servidor de desenvolvimento!!!'
# echo
# echo '---------------' 
# python3 manage.py runserver 8001

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
killall gunicorn
gunicorn ${DJANGO_WSGI_MODULE}:application --name $NAME --workers $NUM_WORKERS --timeout $TIMEOUT --user $USER --bind 127.0.0.1:8000 --bind [::1]:8000 --log-level debug