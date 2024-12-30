#!/bin/bash

if [[ "$1" == "celery" ]]; then
  celery -A src.tasks.celery:celery worker --loglevel=info
elif [[ "$1" == "flower" ]]; then
  celery -A src.tasks.celery:celery flower
fi