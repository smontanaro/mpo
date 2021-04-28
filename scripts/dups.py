#!/usr/bin/env python

"""List duplicate message numbers.

Usage looks something like this:

egrep -i '^message-id:' ham.mbox.cull \\
| awk '{printf("%s %d\\n", $2, NR)}' \\
| python dups.py \\
| sort -r -n

The resulting message numbers give a list of messages in reverse order to
delete from ham.mbox.cull.

"""

import getopt
import sys

def main():
    "see __doc__"

    opts, _args = getopt.getopt(sys.argv[1:], "h")
    for opt, _arg in opts:
        if opt == "-h":
            print(__doc__.strip(), file=sys.stderr)
            return 0

    msgids = set()

    for line in sys.stdin:
        msgid, n = line.strip().split()
        if msgid in msgids:
            print(n, msgid)
        msgids.add(msgid)

if __name__ == "__main__":
    sys.exit(main())
