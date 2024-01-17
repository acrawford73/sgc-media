### ROKU Content Feed

Roku Content feed management system based on Roku Direct Publisher JSON feed specification.

Content data feed provided via JSON API.


### SGC Media Ingest

Upload video content to watch folder.

New files trigger an ingest.

New file metadata added to database.

File information is consumed through API.

Media is consumed via public webserver.

Based on Django 4.2.x


## Install ##

Linux administrator non-root user setup.

Install and configure PostgreSQL database.

```bash
sudo apt-get install postgresql
```

Set password for 'postgres' user, then create database and credentials.

```bash
passwd postgres
su - postgres
createdb database_name
createuser -P database_user
```

Configure database user permissions.

```bash
psql
GRANT ALL PRIVILEGES ON DATABASE database_name TO database_user;
ALTER ROLE database_user SET client_encoding TO 'UTF8';
ALTER ROLE database_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE database_user SET timezone TO 'UTC';
\q
exit
```

Install Django Project

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3 python3-dev python3-pip virtualenv ffmpeg
virtualenv -p /usr/bin/python3 sgc-media
cd sgc-media
```

Copy and configure .env-config file to \~/sgc-media/.env

Set the following (Development) parameters in .env file:

Create secret keys:

- https://django-secret-key-generator.netlify.app/
- https://miniwebtool.com/django-secret-key-generator/
- https://djecrety.ir/

```bash
DEBUG_SECRET_KEY={random_string}
DEBUG_ALLOWED_HOSTS='localhost, 127.0.0.1, {ip_address}'
DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=database_password
DB_HOST=localhost
```

Install packages and migrate database

```bash
source bin/activate
pip install -r requirements.txt
cd src

mkdir -p core/migrations
mkdir -p roku_content/migrations
mkdir -p roku_search/migrations
mkdir -p media/migrations
mkdir -p system_config/migrations

touch core/migrations/__init__.py
touch roku_content/migrations/__init__.py
touch roku_search/migrations/__init__.py
touch media/migrations/__init__.py
touch system_config/migrations/__init__.py

python manage.py makemigrations
python manage.py migrate

python manage.py loaddata roku_content/fixtures/roku_content/*
python manage.py loaddata roku_search/fixtures/roku_search/*
python manage.py loaddata media/fixtures/media/*
python manage.py loaddata core/fixtures/core/*
python manage.py loaddata system_config/fixtures/system_config/*

python manage.py createsuperuser

python manage.py runserver {ip}:8000
```

When ready, set the following (Production) parameters in .env file:

```bash
PRODUCTION=True
PROD_SECRET_KEY={random_string}
PROD_SECRET_KEY_FALLBACK={random_string}
PROD_ALLOWED_HOSTS='domain.com'
SECURE_SSL_HOST='domain.com'
SESSION_COOKIE_DOMAIN='domain.com'
```