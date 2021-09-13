# Normal course of operation #

    1. Download latest unsures:

       bash scripts/process-unsure.sh

       This results in a file named u.mbox in the current directory.

    2. Load that mailbox file into your favorite mail program. Write good
       mails to a file named h.mbox and spam to a file named s.mbox. It's
       typical to simply discard many messages.

    3. Copy s.mbox and h.mbox back to mail.python.org:

       bash scripts/upload.sh

    4. Train on existing and new messages:

       bash scripts/train.sh

    5. Install the result:

       bash scripts/install.sh

    6. Clean up:

       make clean

# Trimming Size of Training Files #

The database tends to grow over time. You can use a couple schemes to reduce
their size without affecting accuracy. Both require the spam.mbox.cull and
ham.mbox.cull files to be downloaded from mail.python.org first. Do that
with:

    bash scripts/get-hamspam.sh

Once that's available, you can identity duplicates of the same message (it
happens sometimes). See the docstring in scripts/dups.py for details. It's
still a work-in-progress, so might need a bit of work.

In addition to deleting duplicate messages, sometimes it makes sense to
delete some messages which aren't duplicates. You can use several
approaches:

    * Delete some number of the oldest messages
    * Delete some random messages
    * Delete a few of the very largest messages

I use the VM mail reader in Emacs which makes some of this fairly
straightforward. It is easy to order the messages by size, date, author,
subject, or a few other schemes. Aside from deleting very old or very large
messages, I choose a sort order which is different than the physical order
of the file, then define a little Emacs macro to help delete every so many
messages. (I like prime numbers, so incorporate a jump of some prime number
of messages after each message delete.) The system is quite
resilient. Still, don't get too carried away deleting messages.

Once you have finished trimming the ham.mbox.cull and spam.mbox.cull mailbox
files, return them to mail.python.org:

    bash scripts/put-hamspam.sh

VM inserts some special message headers to retain information about the
previous processing of the mailbox. The above script strips out those
headers before upload. YMMV if you use a different mail program.

Finally, train and install as above.

# Analyzing Logs

The scripts directory contains two scripts to help generate useful
summaries of data from the mpo-smtpd log files. `classify.py`
classifies the records in one or more log files based on the action
taken, emitting a CSV file with one row per day. `get-mpo-logs.sh`
grabs the current collection of log files from `mail.python.org`,
renaming them to be unique by date. The normal scheme is to run

    bash scripts/get-mpo-logs.sh
    python scripts/classify.py logs/*

with the output of the second command directed to a CSV file or to a
[program which can plot CSV files](https://github.com/smontanaro/csvprogs/blob/main/mpl/src/mpl.py).
Since a week's worth of log files are stored on the server, the
`get-mpo-logs.sh` script need only be run weekly to construct a full
group of log files. Unfortunately, running that script from cron might
be challenging, as it will require entry of your private ssh key.
