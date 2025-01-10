#!/bin/sh

cd src

# Dump Fixtures

python manage.py dumpdata media.mediaaudioformat > media/fixtures/media/mediaaudioformat.json
python manage.py dumpdata media.mediaaudioservice > media/fixtures/media/mediaaudioservice.json
python manage.py dumpdata media.mediacategory > media/fixtures/media/mediacategory.json
python manage.py dumpdata media.mediacountry > media/fixtures/media/mediacountry.json
python manage.py dumpdata media.mediadocformat > media/fixtures/media/mediadocformat.json
python manage.py dumpdata media.mediadocservice > media/fixtures/media/mediadocservice.json
python manage.py dumpdata media.mediaphotoformat > media/fixtures/media/mediaphotoformat.json
python manage.py dumpdata media.mediaphotoservice > media/fixtures/media/mediaphotoservice.json
python manage.py dumpdata media.mediatag > media/fixtures/media/mediatag.json
python manage.py dumpdata media.mediavideoformat > media/fixtures/media/mediavideoformat.json
python manage.py dumpdata media.mediavideogenre > media/fixtures/media/mediavideogenre.json
python manage.py dumpdata media.mediavideoservice > media/fixtures/media/mediavideoservice.json
