#!/bin/sh
set -e

if [ "$1" == "#" ] ; then
    shift
fi

chown -R daemon:daemon .
export \
    ETCD_BIND_ADDR="${ETCD_BIND_ADDR:-0.0.0.0:4001}" \
    ETCD_DATA_DIR="`pwd`" \
    ETCD_NAME="`hostname`"
exec su daemon \
    -c "set -x ; exec /opt/etcd-v0.2.0-Linux-x86_64/etcd \"\${@}\"" \
    -- etcd "${@}"
