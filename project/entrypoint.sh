#!/bin/sh
gunicorn --workers 1 -b :5000 --access-logfile - --error-logfile - project.manage:app