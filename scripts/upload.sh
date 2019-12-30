#!/bin/bash

# Upload latest [sh].mbox files

touch s.mbox h.mbox
scp -C [sh].mbox mail.python.org:/tmp
