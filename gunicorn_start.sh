#!/bin/bash

HOME_PATH=/home/honguyenthanhvinh/PycharmProjects/DjangoProjects/
PROJECT_NAME=ReactorCenterWebsite
DJANGODIR=$HOME_PATH$PROJECT_NAME
SOCKFILE=$HOME_PATH"run/gunicorn.sock"
USER=honguyenthanhvinh
GROUP=honguyenthanhvinh
NUM_WORKERS=1
DJANGO_SETTINGS_MODULE=$PROJECT_NAME".settings"
DJANGO_WSGI_MODULE=$PROJECT_NAME".wsgi"

echo "Starting $PROJECT_NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source $HOME_PATH"venv/bin/activate"
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $HOME_PATH"venv/bin/gunicorn" $DJANGO_WSGI_MODULE:application \
  --name $PROJECT_NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
