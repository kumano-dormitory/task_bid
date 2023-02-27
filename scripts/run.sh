#!/bin/bash

cd /usr/src/app/app && python initdb.py && uvicorn main:app --reload --port=8000 --host=0.0.0.0