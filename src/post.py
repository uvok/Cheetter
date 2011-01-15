#!/usr/bin/python
# -*- coding: utf-8 -*-

from header import *
import os

if len(os.sys.argv)>1:
    msg=" ".join(os.sys.argv[1:])
    print "Sending message:", msg, "\nokay?"
    try:
        raw_input()
    except KeyboardInterrupt:
        print "Abbruch"
        exit()
else:
    msg = raw_input("Status?: ")
succ = chirp.PostUpdates(str(msg), u'\u2026'.encode('utf-8'))
for i in succ:
    print succ.__dict__
