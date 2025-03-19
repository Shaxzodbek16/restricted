#!/bin/bash

black .

pip freeze > requirements.txt

export PYTHONPATH=/Users/shaxzodbek/Developer/restricted


python app/server/server.py


