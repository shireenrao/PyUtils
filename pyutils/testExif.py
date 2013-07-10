#!/usr/bin/env python

import sys
import EXIF
import datetime
import os.path, time

filename = sys.argv[1]
f = open(filename, 'rb')
tags = EXIF.process_file(f)
f.close()
date_str = tags['EXIF DateTimeOriginal'].values
date_obj = datetime.datetime.strptime(date_str,'%Y:%m:%d %H:%M:%S')

print date_obj.year
print date_obj.month
print date_obj.day

print "created: %s" % time.ctime(os.path.getctime(filename))