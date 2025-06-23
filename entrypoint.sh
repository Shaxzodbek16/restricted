#!/bin/bash

black .

pip freeze > requirements.txt

 export PYTHONPATH="$(pwd)"

python app/server/server.py
