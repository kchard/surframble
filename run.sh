#1/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ZMQ_DIR="$SCRIPT_DIR/zmq"
UWSGI_DIR="$SCRIPT_DIR/uwsgi"

cd $ZMQ_DIR && ./run.sh
cd $UWSGI_DIR && ./run.sh
