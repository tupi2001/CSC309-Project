#!/usr/bin/env bash
-m venv .  # creates a new venv
source env/bin/activate  # activates the new venv
cd ./PB/course_project
pip install -r requirements.txt  # installs the requirements
python3 manage.py makemigrations
python3 manage.py migrate

cd ../../frontend/
npm install
