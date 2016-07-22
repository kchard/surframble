#!/bin/bash

set -o errexit
set -o nounset

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

crontab $SCRIPT_DIR/../config/livecron
