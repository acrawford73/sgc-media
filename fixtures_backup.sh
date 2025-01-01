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

python manage.py dumpdata roku_content.ratingcountry > roku_content/fixtures/roku_content/ratingcountry.json
python manage.py dumpdata roku_content.creditrole > roku_content/fixtures/roku_content/creditrole.json
python manage.py dumpdata roku_content.externalidtype > roku_content/fixtures/roku_content/externalidtype.json
python manage.py dumpdata roku_content.genre > roku_content/fixtures/roku_content/genre.json
python manage.py dumpdata roku_content.language > roku_content/fixtures/roku_content/language.json
python manage.py dumpdata roku_content.parentalrating > roku_content/fixtures/roku_content/parentalrating.json
python manage.py dumpdata roku_content.rating > roku_content/fixtures/roku_content/rating.json
python manage.py dumpdata roku_content.ratingsource > roku_content/fixtures/roku_content/ratingsource.json
python manage.py dumpdata roku_content.videotype > roku_content/fixtures/roku_content/videotype.json
