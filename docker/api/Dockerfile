FROM python:3.11.1-bullseye

RUN apt-get update \
    && apt-get install -y default-mysql-client \
    && apt-get -y install gcc libmariadb-dev \
    && apt-get install --no-install-recommends -y tzdata \
    && apt-get clean

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY requirements.txt .

RUN pip install -U pip \
   && pip install --no-cache-dir --upgrade -r requirements.txt

