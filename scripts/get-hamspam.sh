#!/bin/bash

# Pull spam and ham mailboxes from mpo...  We copy the cull versions, as
# they are the output of the last training effort and will be the start of
# the next.  Also pull the latest log file for debugging.
ssh mail.python.org \
    sudo bash -c '"cd /usr/local/spambayes-corpus ; tar cfj - {spam,ham}.mbox.cull tte.log"' \
    | tar xvfj -
