# syntax=docker/dockerfile:1

FROM python:3.9-alpine

# lets just be nice and tell docker the port we're exposing (not required)
EXPOSE 4040 

# install git using apk (alpine's package manager)
RUN apk add --no-cache git

# set directory to /usr/src/app
WORKDIR /usr/src/app

# install requirements.txt first so installs can be cached
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# copy code into the image
COPY . .

# run the code
CMD [ "python3", "./app.py" ]