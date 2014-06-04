#!/bin/sh

trap "echo CCCCCCC 2" 2
trap "echo CCCCCCC 3" 3
trap "echo CCCCCCC 4" 4
trap "echo CCCCCCC 5" 5
trap "echo CCCCCCC 6" 6
trap "echo CCCCCCC 9" 9
trap "echo CCCCCCC 15" 15
httpd
qdrouterd &
tail -f /var/log/httpd/*


