#!/bin/sh

set -e

python manage.py test
py.test */test_*.py
