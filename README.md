# COVID Tracker

# Roles
- Frontend: Ken Lin, Daniel Kibatullin 
- Backend: Tejas Siddaramaiah
- Testing: All

# Description

Description: This website retrieves and display data regarding COVID. It covers a wide list of countries if not all. Each country has data all the way from February 2nd, 2023 all the way to today. This website is always up to date and displays data such as cases, deaths, and tests. In addition, you can sign up for daily notifications. You can select as many countries as you like. Each day, you will receive data regarding total deaths, new deaths, new infected, total infected, critical cases, recovered cases, cases per 1 million people, total test, and test per 1 million people.

# API 

https://rapidapi.com/api-sports/api/covid-193
- Path: '/history', '/countries'

# Launch Code

## Install the Prerequisites

sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

curl https://pyenv.run | bash

export PATH="$HOME/.pyenv/bin:$PATH"
      eval "$(pyenv init --path)"
      eval "$(pyenv virtualenv-init -)"
    
pyenv install –list

pyenv update

pyenv install 3.11.5

pyenv local 3.11.5

python -m venv env_3.11.5

## Run the Website

You must go to the countries tab and press the "Fetch Countries" button to populate the database with all the countries.

In each country detail, you must select a calendar date and press the button "Fetch Data" to access the COVID-19 information for that date. Since, we are limited to 60 requests per minute, you must separately pick each date that you want for each country.

For the secrets.json, we have given a template that you must follow to be able to properly run the website. For the email and app password, you must make an app password for the gmail account you want to send emails from. Some more info: https://medium.com/@muhizia4/sending-an-email-using-gmail-account-as-smtp-server-with-django-app-94c3a75b9e40

## Running Virtual Env

source env_3.11.5/bin/activate (Mac/Linux) or env_3.11.5\Scripts\activate (Windows)

pip install --upgrade pip-tools pip setuptools wheel
pip-compile --upgrade --generate-hashes --output-file requirements_env/main.txt requirements_env/main.in
pip-compile --upgrade --generate-hashes --output-file requirements_env/dev.txt requirements_env/dev.in

pip-sync requirements_env/main.txt requirements_env/dev.txt

## Database Code

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

Go to http://localhost:8000/countries/

(Note: In Countries List, you need to click the name since its not a button. Just a list with CSS)
(Note: Most of the countries doesn't have saved date. USA has all the data though all the way to 02/02/2023)

## Daily Notifications

In terminal edit crontab with 'crontab -e' in terminal.

Enter the following command in the vim window to send daily COVID notifications at 7:30 AM: '30 7 * * * /path/to/FinalProject/env_3.11.5/bin/python /path/to/FinalProject/covid/manage.py sendnotifications'

