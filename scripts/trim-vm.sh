#!/bin/bash

mbox=$1

cat $mbox \
    | formail -d -s formail -I X-VM-v5-Data: -I X-VM-Summary-Format: \
              -I X-VM-Labels: -I X-VM-VHeader: -I X-VM-Last-Modified: \
              -I X-VM-IMAP-Retrieved: -I X-VM-POP-Retrieved: \
              -I X-VM-Bookmark -I X-VM-Message-Order: \
> $mbox.clean

newsz=$(wc -c < $mbox.clean)
oldsz=$(wc -c < $mbox)
frac=$(python3 -c "print(f'{100*${newsz}/${oldsz}:.0f}')")
if [ $frac -gt 90 ] ; then
    mv $mbox $mbox.save
    mv $mbox.clean $mbox
else
    echo "Something went horribly wrong while cleaning VM headers."
    exit 1
fi
