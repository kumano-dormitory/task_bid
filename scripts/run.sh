#!/bin/bash

cd /usr/src/app/app && uvicorn main:app --reload --port=8000 --host=0.0.0.0