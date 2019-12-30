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

In addition to simply deleting duplicate messages, sometimes it makes sense
to simply delete some of the messages. You can use several approaches:

    * Delete some number of the oldest messages
    * Delete some random messages
    * Delete a few of the very largest messages

I use the VM mail reader in Emacs which makes some of this fairly
straightforward. It is easy to order the messages by size, date, author,
subject, or a few other schemes. Aside from deleting very old or very large
messages, I choose a sort order which is different than the physical order
of the file, then define a little Emacs macro to help delete every so many
messages.

Once you have finished trimming the ham.mbox.cull and spam.mbox.cull mailbox
files, you return them to mail.python.org:

    bash scripts/put-hamspam.sh

VM inserts some special message headers to retain information about the
previous processing of the mailbox. The above script strips out those
headers before upload. YMMV if you use a different mail program.
