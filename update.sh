#!/usr/bin/env bash
cp -rf ../repositories/quality2/** ./
echo 'from quality2.wsgi import application' > passenger_wsgi.py
