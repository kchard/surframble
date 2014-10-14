#!/bin/bash
kill_process()
{
    PID=$(ps -ef | grep "$1" | grep -v grep | awk '{print $2}')

    if [ -n "$PID" ]; then
        echo "killing process '$1' with PID: $PID"
    kill -9 $PID
    fi
}

mkdir -p logs
kill_process uwsgi
uwsgi --socket 127.0.0.1:9090 --wsgi-file buoy.py --master > logs/buoy.py 2>&1 &
