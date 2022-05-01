#!/bin/sh

docker run -it --rm\
    -v "/$PWD":/usr/src/dockerz\
    -v //var/run/docker.sock:/var/run/docker.sock\
    --network="pog.network"\
    -p 5000:5000\
    -w //usr/src/dockerz\
    python:3.10-alpine\
    sh -c "apk add git && pip install -r requirements.txt && python app.py"