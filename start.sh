#!/usr/bin/env bash
python3 sqlsetup.py
service nginx start
uwsgi --ini uwsgi.ini