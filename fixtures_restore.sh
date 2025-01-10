#!/bin/sh

cd src

# Restore Fixtures

python manage.py loaddata media/fixtures/media/*

