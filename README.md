# Microservice Django #

### Introduction ###

The project allows you to manage conference rooms. 
It was created in order to improve the skills of the Django framework.

### Technology stack ###
Python 3.8.5, Django, Git, HTML

### Requirements ###
* Python3.8.5
* Unoccupied port 8000

### Prepare virtualenv (Linux) ###

* Prepare directory for virtual env (on the root of project):
	`mkdir venv`
* Prepare virtual env module:
	`sudo apt-get install python3-venv`
* Create venv:
	`python3 -m venv ./venv/`
* Checkout to venv:
	`source ./venv/bin/activate`
* Install requirements:
	`pip install -r requirements.txt`
* Check requirements:
	`pip list`

### Run application locally ###

* Source the virtaul enviroment:
	`source ./vevn/bin/activate`
* Migrate:
	`python3 manage.py migrate`
* Run django application:
	`python3 manage.py runserver`