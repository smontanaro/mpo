#!/bin/bash

# incorporate new spam/ham messages into corpus and retrain. [sh].mbox are
# already assumed to have been copied to mpo:/tmp.
ssh mail.python.org \
          sudo bash -c '"cd /usr/local/spambayes-corpus ; sh install.sh"'
