FROM python:3.11.1-bullseye

RUN apt update \
    && apt install -y default-mysql-client \
    && apt-get -y install gcc libmariadb-dev \
    && apt install --no-install-recommends -y tzdata \
    && apt clean

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY requirements.txt .

RUN pip install -U pip \
   && pip install --no-cache-dir --upgrade -r requirements.txt

