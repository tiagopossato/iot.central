#!/bin/bash

NAME="central"                              #Name of the application (*)  
DJANGODIR=/home/tiago/iot.central/central             # Django project directory (*)  
SOCKFILE=/home/tiago/iot.central/central/run/gunicorn.sock        # we will communicate using this unix socket (*)  
USER=tiago                                       # the user to run as (*)  
GROUP=tiago                                     # the group to run as (*)  
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn (*)  
DJANGO_SETTINGS_MODULE=central.settings             # which settings file should Django use (*)  
DJANGO_WSGI_MODULE=central.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR  
source /home/tiago/centralenv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE  
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)  
test -d $RUNDIR || mkdir -p $RUNDIR

echo '---------------'
echo
echo 'servidor de desenvolvimento!!!'
echo
echo '---------------' 
python3 manage.py runserver 8001

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

#/home/tiago/centralenv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application --name $NAME --workers $NUM_WORKERS --user $USER --bind 127.0.0.1:8000 --bind [::1]:8000
#--bind=unix:$SOCKFILE