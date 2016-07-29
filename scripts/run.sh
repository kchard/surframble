#!/bin/bash

set -o errexit
set -o nounset

docker-compose down
docker-compose build
docker-compose up -d

