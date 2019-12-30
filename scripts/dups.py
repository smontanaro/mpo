#!/usr/bin/env python

"""List duplicate message numbers.

Usage looks something like this:

egrep -i '^message-id:' ham.mbox.cull \\
| awk '{print $2}' \\
| awk '{printf("%s %d\n", $2, NR)}'
| python dups.py \\
| sort -r -n

The resulting message numbers give a list of messages in reverse order to
delete from ham.mbox.cull.

"""

import sys

def main():
    "see __doc__"

    msgids = set()

    for line in sys.stdin:
        msgid, n = line.strip().split()
        if msgid in msgids:
            print(n)
        msgids.add(msgid)

if __name__ == "__main__":
    sys.exit(main())
