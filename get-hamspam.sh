#!/bin/bash

# Pull spam and ham mailboxes from mpo...
ssh mail.python.org \
    sudo bash -c '"cd /usr/local/spambayes-corpus ; tar cfj - {spam,ham}.mbox"' \
    | (cd $(dirname $0) ; tar xvfj -)

emacs --eval '(vm-visit-folder "ham.mbox")'
