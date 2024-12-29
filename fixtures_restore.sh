#!/bin/sh

cd src

# Restore Fixtures

python manage.py loaddata media/fixtures/media/*

python manage.py loaddata roku_content/fixtures/roku_content/*
