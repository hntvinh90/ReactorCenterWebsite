#!/bin/bash

USER=honguyenthanhvinh
GROUP=$USER
HOME_PATH=/home/$USER"/PycharmProjects/DjangoProjects/"
PROJECT_NAME=ReactorCenterWebsite
DJANGODIR=$HOME_PATH$PROJECT_NAME
SOCKFILE=$HOME_PATH"gunicorn.sock"
NUM_WORKERS=1
DJANGO_SETTINGS_MODULE=$PROJECT_NAME".settings"
DJANGO_WSGI_MODULE=$PROJECT_NAME".wsgi"
VIRTUALENV_PYTHON=$HOME_PATH"venv/bin/"

echo "Starting $PROJECT_NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source $VIRTUALENV_PYTHON"activate"
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $VIRTUALENV_PYTHON"gunicorn" $DJANGO_WSGI_MODULE:application \
  --name $PROJECT_NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE

