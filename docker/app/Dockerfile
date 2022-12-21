FROM python:3.11-alpine

WORKDIR /usr/src/server

ADD requirements.txt .

RUN apk add --no-cache build-base bash mariadb-client mariadb-connector-c-dev
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

