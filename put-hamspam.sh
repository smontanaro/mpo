#!/bin/bash

cd $(dirname $0)

# Push spam and ham mailboxes to mpo...

# Clean off the VM message cruft.
bash trim-vm.sh ham.mbox
bash trim-vm.sh spam.mbox

# Rename the mbox files temporarily, as the .cull versions are the end of
# the training process. The train script picks up from there and renames
# them to {ham,spam}.mbox before training proper begins.
mv spam.mbox spam.mbox.cull
mv ham.mbox ham.mbox.cull
tar cfz - {spam,ham}.mbox.cull \
    | ssh mail.python.org \
          sudo bash -c '"cd /usr/local/spambayes-corpus ; tar xvfz -"'
mv spam.mbox.cull spam.mbox
mv ham.mbox.cull ham.mbox
