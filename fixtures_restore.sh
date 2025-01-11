#!/bin/sh

echo
echo "Please enter the virtual environment before running."
echo

cd src

# Restore Fixtures

python manage.py loaddata media/fixtures/media/*

