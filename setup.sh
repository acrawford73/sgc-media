#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python3 python3-dev python3-pip virtualenv
sudo apt-get install -y ffmpeg postgresql git gh

gh auth login   
gh repo clone acrawford73/sgc-media

# DB - enter manually
sudo vi /etc/postgresql/14/main/pg_hba.conf
sudo systemctl restart postgresql
sudo systemctl status postgresql
sudo passwd postgres
su - postgres
createdb sgcdev
createuser -P sgc
psql
GRANT ALL PRIVILEGES ON DATABASE sgc TO sgc;
ALTER ROLE sgc SET client_encoding TO 'UTF8';
ALTER ROLE sgc SET default_transaction_isolation TO 'read committed';
ALTER ROLE sgc SET timezone TO 'UTC';
\q
exit

# Env
virtualenv -p /usr/bin/python3 sgc-media
cd sgc-media/
source bin/activate
pip install -r requirements.txt

cd src
mkdir -p roku_content/migrations
mkdir -p roku_search/migrations
mkdir -p system_config/migrations
mkdir -p core/migrations
mkdir -p media/migrations
touch roku_content/migrations/__init__.py
touch roku_search/migrations/__init__.py
touch core/migrations/__init__.py
touch media/migrations/__init__.py
touch system_config/migrations/__init__.py

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py loaddata roku_content/fixtures/roku_content/ratingsource
python manage.py loaddata roku_content/fixtures/roku_content/parentalrating
python manage.py loaddata roku_content/fixtures/roku_content/rating
python manage.py loaddata roku_content/fixtures/roku_content/genre
python manage.py loaddata roku_content/fixtures/roku_content/creditrole
python manage.py loaddata roku_content/fixtures/roku_content/credits
python manage.py loaddata roku_content/fixtures/roku_content/videotype
python manage.py loaddata roku_content/fixtures/roku_content/language
python manage.py loaddata roku_content/fixtures/roku_content/externalidtype
python manage.py loaddata roku_content/fixtures/roku_content/country
python manage.py loaddata media/fixtures/media/*
