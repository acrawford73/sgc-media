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

Install and configure PostgreSQL database.

Install Django app (Development):

```bash
sudo apt-get install python3 python3-dev python3-pip virtualenv ffmpeg

virtualenv -p /usr/bin/python3 sgc-media

# Copy and configure .env-config file to \~/sgc-media/.env
# Create secret keys:
#  https://django-secret-key-generator.netlify.app/
#  https://miniwebtool.com/django-secret-key-generator/
#  https://djecrety.ir/

cd sgc-media
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

Install Django app (Production):

TBD