#!/usr/bin/env bash

usage () {
    echo "Use: ./run.sh [dev|prod|stop]"
}

if [ "$#" == 0 -o "$1" == "-h" -o "$1" == "--help" ]
then
    echo "Django Coleman HTTP Server startup script application."
    usage
    exit 1
fi

if [ -z "$PID_FILE" ]; then
    PID_FILE="/tmp/dcoleman-master.pid"
fi

if [ -z "$PORT" ]; then
    PORT="8000"
fi

case "$1" in
    dev)
        export DEBUG=True
        python3 manage.py runserver 0:$PORT
        ;;
    prod)
        echo -n "Starting uWSGI server for Django Coleman... "
        if [ "$DEBUG" == "True" -o "$DEBUG" == "true" -o "$DEBUG" == "1"  ]
        then
          echo -n " (WARNING: setting DEBUG is enabled)  "
        fi
        uwsgi --module=coleman.wsgi:application \
              --master --pidfile=$PID_FILE \
              --http=0:$PORT \
              --processes=5 \
              --max-requests=5000 \
              --vacuum \
              --daemonize=dcoleman.log
        sleep 0.7
        echo "started with PID $(cat $PID_FILE)"
        echo "Serving at http://localhost:8000/"
        ;;
    stop)
        if [ -f "$PID_FILE" ]
        then
            PID="$(cat $PID_FILE)"
            echo -n "Stopping uWSGI server for Django Coleman with PID $PID... "
            kill -9 "$PID" && rm "$PID_FILE"
            echo "done"
        else
          echo "No uWSGI server for Django Coleman found" >&2
          exit 1
        fi
        ;;
    *)
        echo "./run ERROR: unknown '$1' option." >&2
        usage
        exit 2
        ;;
esac
