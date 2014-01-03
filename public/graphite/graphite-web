#!/bin/sh
set -e

cd /opt/graphite/webapp/graphite

python2.7 manage.py syncdb --noinput
mkdir -p /opt/graphite/storage/log/webapp /opt/graphite/storage/var/webapp
chown -R graphite:graphite /opt/graphite/storage/
set -x
exec /usr/local/bin/gunicorn_django -u graphite -g graphite -b 0.0.0.0:8080 /opt/graphite/webapp/graphite/settings.py
