#!/bin/bash

init()
{
    mkdir -p logs
}

kill_process()
{
    PID=$(ps -ef | grep "$1" | grep -v grep | awk '{print $2}')

    if [ -n "$PID" ]; then
        echo "killing process '$1' with PID: $PID"
        kill $PID
    fi
}

start()
{
    init
    echo "starting process '$1.py'"
    python "$1.py" >> "logs/$1.log" 2>&1 &
}

stop()
{
    kill_process "$1.py" 
}

restart()
{
   stop $1 && start $1 
}

case $1 in
    start)
        start broker && start buoy_to_json && start buoy_to_mongo && start buoy_to_xml
        ;;
    stop)
        stop broker ; stop buoy_to_json ; stop buoy_to_mongo ; stop buoy_to_xml

        ;;
    restart)
        restart broker && restart buoy_to_json && restart buoy_to_mongo && restart buoy_to_xml

        ;;
    *)
        restart broker && restart buoy_to_json && restart buoy_to_mongo && restart buoy_to_xml

        ;;
esac
