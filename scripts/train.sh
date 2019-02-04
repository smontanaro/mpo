#!/bin/bash

# incorporate new spam/ham messages into corpus and retrain. [sh].mbox are
# already assumed to have been copied to mpo:/tmp.
ssh mail.python.org \
          sudo bash -c '"cd /usr/local/spambayes-corpus
if [ -f /tmp/h.mbox ] ; then
    cat /tmp/h.mbox >> ham.mbox.cull
fi
mv ham.mbox.cull ham.mbox
if [ -f /tmp/s.mbox ] ; then
    cat /tmp/s.mbox >> spam.mbox.cull
fi
mv spam.mbox.cull spam.mbox
sh train.sh"'
