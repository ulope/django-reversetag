#!/bin/sh

PYTHONPATH=.:.. django-admin.py test revtest --settings=test_settings

