#!/usr/bin/env bash
cp -rf ../repositories/quality2/** ./
python update_passenger_wsgi.py
