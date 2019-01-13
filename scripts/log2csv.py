#!/usr/bin/env python

"""Process mpo-smtpd.log file from stdin, write to stdout as CSV.

Output is a CSV file with the following fields:

sender - sender email (left of '@')
sender-domain sender email domain (right of '@')
sender-host
recipient - recipient email (left of '@')
recipient-domain - recipient domain (right of '@')
score - SpamBaye score (if the message was scored)
message-id
file - output file (if the message was saved as unsure)
action - end result
greylist - 'start' or 'end' if message was greylisted

In addition, if the -v flag is given, any SpamBayes clues are added to the
end of the row (single big cell - otherwise unprocessed).
"""

import csv
import getopt
import sys

def main(args):
    "see __doc__"
    verbose = False
    opts, args = getopt.getopt(args, "hv")
    for opt, _arg in opts:
        if opt == "-v":
            verbose = True
        elif opt == "-h":
            print(__doc__.strip(), file=sys.stderr)
            return 0

    records = {}
    rows = []
    for line in sys.stdin:
        pid, rest = line.strip().split(" ", 1)
        try:
            pid = int(pid)
        except ValueError:
            # assume corrupt log record.
            continue
        if rest == "mpo_smtpd.py listening on 0:8025":
            continue
        if pid not in records:
            records[pid] = {"pid": pid}
        rec = records[pid]
        fields = rest.split()
        if fields[0:2] == ["connection", "from"]:
            pass
        elif fields[0:2] == ["mail", "from"]:
            fields[2] = fields[2].replace("'", "")
            if "@" in fields[2]:
                rec["sender"], rec["sender-domain"] = fields[2].split("@", 1)
            else:
                rec["sender"] = fields[2]
        elif fields[0:2] == ["msg", "from"]:
            rec["sender-host"] = fields[2]
        elif fields[0:2] == ["rcpt", "to"]:
            fields[2] = fields[2].replace("'", "")
            if "@" in fields[2]:
                rec["recipient"], rec["recipient-domain"] = fields[2].split("@", 1)
            else:
                rec["recipient"] = fields[2]
        elif fields[0:2] == ["spambayes", "score"]:
            rec["score"] = fields[2]
        elif fields[0:2] == ["spambayes", "clues"]:
            if verbose:
                rec["clues"] = " ".join(fields[2:])
        elif fields[0] == "message-id":
            rec["message-id"] = fields[1]
        elif fields[0:2] in (["message", "accepted"],
                             ["553", "rejected,"]):
            rec["action"] = " ".join(fields)
        elif fields[0:3] == (["553", "invalid", "bounce"]):
            rec["action"] = " ".join(fields)
        elif fields[0:2] == ["delaying", "message"]:
            rec["greylist"] = "start"
        elif fields[0:3] == ["allowing", "delayed", "message"]:
            rec["greylist"] = "end"
        elif fields[0:3] in (["IP", "is", "whitelisted"],
                             ["domain", "is", "whitelisted"],
                             ["421", "temporary", "error,"]):
            pass
        elif fields[0:3] == ["saved", "message", "to"]:
            rec["file"] = fields[3]
        elif fields[0] == "quit":
            rows.append(rec)
        elif fields[0:3] == ["proxy", "error", "data"]:
            rec["action"] = " ".join(fields[3:])
        elif fields[0:3] == ["554", "permanent", "error"]:
            pass
        elif fields[0:2] == ["rejecting", "attachment"]:
            pass
        elif fields[0] == "subject":
            pass
        else:
            print("Unrecognized record:", fields, file=sys.stderr)

    fieldnames = ("pid sender sender-domain sender-host"
                  " recipient recipient-domain score message-id"
                  " file action greylist").split()
    if verbose:
        fieldnames.append("clues")
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
