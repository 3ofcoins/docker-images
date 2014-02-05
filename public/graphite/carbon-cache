#!/bin/sh
set -e

mkdir -p /opt/graphite/storage/whisper 
chown -R graphite:graphite /opt/graphite/storage
rm -f /opt/graphite/storage/carbon-cache-$HOSTNAME.pid
set -x
exec /opt/graphite/bin/carbon-cache.py --debug --instance=$HOSTNAME start
