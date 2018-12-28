#!/bin/bash

# incorporate new spam/ham messages into corpus and retrain. [sh].mbox are
# already assumed to have been copied to mpo:/tmp.
ssh mail.python.org \
          sudo bash -c '"cd /usr/local/spambayes-corpus ; cat /tmp/h.mbox >> ham.mbox.cull ; mv ham.mbox.cull ham.mbox ; cat /tmp/s.mbox >> spam.mbox.cull  ; mv spam.mbox.cull spam.mbox ; sh train.sh"'
