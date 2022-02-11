#!/usr/bin/env bash

usage () {
    echo "Use: ./run.sh [dev|prod]"
}

if [ "$#" == 0 -o "$1" == "-h" -o "$1" == "--help" ]
then
    echo "Django Coleman HTTP Server startup script application."
    usage
    exit 1
fi

case "$1" in
    dev)
        export DEBUG=True
        python3 manage.py runserver 0:8000
        ;;
    prod)
        export DEBUG=False
        if [ -z "$DATABASE_URL" ]
        then
            # Default database, set the real string connection from the environment
            # variable instead of hardcoding here
            export DATABASE_URL="postgresql://dcoleman:postgres@localhost/dcoleman_dev"
        fi
        echo -n "Starting uWSGI server for Django Coleman... "
        uwsgi --module=coleman.wsgi:application \
              --master --pidfile=/tmp/dcoleman-master.pid \
              --http=0:8000 \
              --processes=5 \
              --max-requests=5000 \
              --vacuum \
              --daemonize=dcoleman.log
        sleep 0.7
        echo "started with PID $(cat /tmp/dcoleman-master.pid)"
        ;;
    *)
        echo "./run ERROR: unknown '$1' environment."
        usage
        exit 2
        ;;
esac
