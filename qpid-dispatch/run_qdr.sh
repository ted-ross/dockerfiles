#!/bin/sh

export HOSTNAME_IP_ADDRESS=$(hostname -i)

DOLLAR='$' envsubst < /etc/qpid-dispatch/qdrouterd.conf.template > /tmp/qdrouterd.conf
exec /sbin/qdrouterd --conf /tmp/qdrouterd.conf
