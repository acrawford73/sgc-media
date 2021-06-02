### SGC Media Ingest

Upload video content to watch folder

New files trigger an ingest

New file metadata added to database

File information is consumed through API

Media is consumed via public webserver

Django 3.2.3

## Install ##

```bash
sudo apt-get install python python-dev python-pip virtualenv
virtualenv -p /usr/bin/python3 sgc-media
cd sgc-media
source bin/activate
cd src
python manage.py runserver
```
