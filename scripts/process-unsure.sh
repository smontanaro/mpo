#!/bin/bash

# Pull unsure mail from the SpamBayes setup...
ssh mail.python.org \
    sudo bash -c '"cd /var/spool/spambayes/unsure ; tar cf - . ; rm *.msg"' \
    | tar xvf -

# Construct an mbox file from them...
rm -f u.mbox
for f in *.msg ; do
    cat $f >> u.mbox
    echo "" >> u.mbox
done
rm *.msg

# And riffle through them to sort into spam and ham.
emacs --eval '(vm-visit-folder "u.mbox")'
