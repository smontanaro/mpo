#!/bin/bash

# Push spam and ham mailboxes to mpo...

# The .cull versions of the mailboxes are the output of the training script,
# and are thus the starting point for the next cycle.
# Clean off the VM message cruft.
bash $(dirname $0)/trim-vm.sh ham.mbox.cull && \
bash $(dirname $0)/trim-vm.sh spam.mbox.cull && \
tar cfj - {spam,ham}.mbox.cull \
    | ssh mail.python.org \
          sudo bash -c '"cd /usr/local/spambayes-corpus ; tar xvfj -"'
