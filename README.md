### SGC Media Ingest

Upload video content to watch folder

New files trigger an ingest

New file metadata added to database

File information is consumed through API

Media is consumed via public webserver

Django 4.2.x

## Install ##

```bash
sudo apt-get install python3 python3-dev python3-pip virtualenv ffmpeg
virtualenv -p /usr/bin/python3 sgc-media
cd sgc-media
source bin/activate
cd src
python manage.py runserver {ip}:8000
```
