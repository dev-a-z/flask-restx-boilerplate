#!/bin/bash
export PYTHONPATH="${FLASK_BOILERPLATE_DIR}/app"
export FLASK_APP="app.py"
export FLASK_ENV="production"
flask run --host 0.0.0.0
