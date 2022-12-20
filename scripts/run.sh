#!/bin/bash
echo "Waiting for mysql to start ..."
until mysql -h"$MYSQL_HOST" -u "$MYSQL_USER" -p "$MYSQL_PASSWORD" &> /dev/null
do 
    sleep 1
done

cd /workspace/app && uvicorn main:app --reload --port=8080 --host=0.0.0.0