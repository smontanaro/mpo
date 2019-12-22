#!/usr/bin/env python

"""List duplicate message numbers.

Input is the result of this shell pipeline:

cat ham.mbox.cull \\
| formail -s md5sum \\
| awk '{printf("%s %010d\n", $0, NR)}'

so input will look something like this:

5c579810d25f20d7117ee6c4cf797e30  - 1
13b585d039fb5936fa800be14219ed8d  - 2
ab2eec6316c2b157ca2ef0d0009b3ee0  - 3
a4743dcb2e0aaa44c0b3dcc91545a044  - 4
...

For every checksum which is repeated, emit the duplicate message number. A
full pipeline would look something like this:

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
