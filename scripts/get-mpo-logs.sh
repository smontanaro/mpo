#!/bin/bash

cd $(dirname $0)/..

ssh mail.python.org 'sudo cp -p /var/log/upstart/mpo-smtpd.log* /tmp'
ssh mail.python.org 'sudo chmod 644 /tmp/mpo-smtpd.log*'

scp -p mail.python.org:'/tmp/mpo-smtpd.log*' logs

ssh mail.python.org 'sudo rm /tmp/mpo-smtpd.log*'

gzip logs/mpo-smtpd.log

for f in logs/mpo-smtpd*.gz ; do
    dt=$(date -r $f +%Y%m%d)
    mv $f logs/${dt}-mpo-smtpd.log.gz
done
