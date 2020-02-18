#!/bin/bash

# Upload latest [sh].mbox files

# Always touch in case our processing didn't write to one file or the
# other. This guarantees that the mpo version of both files is always
# new. Otherwise the training script would tend to duplicate recently
# uploaded messages.

touch s.mbox h.mbox
bash $(dirname $0)/trim-vm.sh h.mbox && \
bash $(dirname $0)/trim-vm.sh s.mbox && \
scp -C [sh].mbox mail.python.org:/tmp
