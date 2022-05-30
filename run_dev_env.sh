#!/usr/bin/env bash

export FLASK_APP=status_page_app
export FLASK_ENV=development
source .env

flask run --port=8080 --host=0.0.0.0