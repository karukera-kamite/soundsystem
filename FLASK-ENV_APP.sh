#!/bin/bash
source ../bin/activate
export FLASK_APP=router.py
export FLASK_ENV=development
flask run
