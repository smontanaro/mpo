#!/usr/bin/env python

"""Classify message actions for logfile(s) on command line.

There are several possible action messages:

553 rejected, executable attachment.
553 rejected, message looks like spam.
553 rejected (put NOTSPAM in message subject to bypass spam filter)
message accepted
message accepted (filters bypassed)
message accepted (msg from localhost)
message accepted (spambayes bypassed)

We want to count all of them. Output is a CSV file on stdout which can
be fed into other tools. Column headers correspond to the above patterns:

pattern                                   column name
-------                                   -----------
553 rejected, executable attachment.      reject-exec
553 rejected, message looks like spam.    reject-spam
553 rejected (put NOTSPAM in message ...  reject-other
message accepted                          accept
message accepted (filters bypassed)       accept-filtbyp
message accepted (msg from localhost)     accept-local
message accepted (spambayes bypassed)     accept-sbbyp

In addition there is a date column which corresponds to the date of
the file. (mpo-smtpd doesn't include timestamps in its log messages.)

"""

import csv
import datetime
import gzip
import os
import pathlib
import re
import sys

def open_smart(fname, mode="rt"):
    "open regular or gzipped files"
    if fname.endswith(".gz"):
        return gzip.open(fname, mode=mode)
    return open(fname, mode=mode)

SPAM = 0.70
HAM = 0.20

# Note that the order of fieldnames and patterns must match...
FIELDNAMES = ("date reject-exec reject-spam reject-other"
              " accept-filtbyp accept-local accept-sbbyp accept"
              " delayed unsure"
              " reject-all accept-all total").split()
PATTERNS = [
    "[0-9]+ DATE zzyzx",    # should never match!
    "[0-9]+ 553 rejected, executable attachment[.]",
    "[0-9]+ 553 rejected, message looks like spam[.]",
    "[0-9]+ 553 rejected [(]put NOTSPAM in message subject to bypass spam filter[)]",
    "[0-9]+ message accepted [(]filters bypassed[)]",
    "[0-9]+ message accepted [(]msg from localhost[)]",
    "[0-9]+ message accepted [(]spambayes bypassed[)]",
    "[0-9]+ message accepted",
    "[0-9]+ delaying message",
    "[0-9]+ UNSURE zzyzx",  # should never match!
    "[0-9]+ REJECT zzyzx",  # should never match!
    "[0-9]+ ACCEPT zzyzx",  # should never match!
    "[0-9]+ TOTAL zzyzx",   # should never match!
    ]

PAT_NAMES = list(zip(PATTERNS, FIELDNAMES))

def main():
    "See __doc__"

    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDNAMES)
    writer.writeheader()
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            for fname in sorted(os.listdir(arg)):
                writer.writerow(classify(os.path.join(arg, fname)))
        else:
            writer.writerow(classify(arg))

def classify(fname):
    counts = dict(zip(FIELDNAMES, [0] * len(FIELDNAMES)))
    path = pathlib.Path(fname)
    date = datetime.datetime.fromtimestamp(path.stat().st_mtime).date()
    counts["date"] = str(date)
    with open_smart(str(path)) as mpo_log:
        for line in mpo_log:
            if "spambayes score" in line:
                score = float(line.strip().split()[-1])
                if HAM < score < SPAM:
                    counts["unsure"] += 1
            else:
                for (pat, name) in PAT_NAMES:
                    if re.match(pat, line) is not None:
                        counts[name] += 1
                        counts["total"] += 1
                        break
    counts["accept-all"] = sum(counts[key] for key in counts if "accept" in key)
    counts["reject-all"] = sum(counts[key] for key in counts if "reject" in key)
    return counts

if __name__ == "__main__":
    sys.exit(main())
