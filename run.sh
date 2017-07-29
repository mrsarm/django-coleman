#!/usr/bin/env bash

usage () {
    echo
    echo "Use: ./run.sh [dev|prod]"
    echo
}

if [ "$#" == 0 -o "$1" == "-h" -o "$1" == "--help" ]
then
    echo
    echo "Startup script application."
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
        python3 manage.py runserver 0:8000 --insecure
        ;;
    *)
        echo
        echo "./run ERROR: unknown '$1' environment."
        echo
        usage
        exit 2
        ;;
esac
