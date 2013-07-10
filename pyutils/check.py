#!/usr/bin/env python

import os, sys, errno
import exiftool

_source = "/Users/shireenrao/Desktop/test"
#files = ["IMG_0740.CR2", "IMG_0378.JPG", "IMG_1323.JPG"]
files = ["IMG_0508.JPG"]
#fileList = []
#for root, dirs, files in os.walk(_source):
#    for name in files:
#        filename = os.path.join(root,name)
#        if filename.lower().endswith('.jpg'):
#            fileList.append(filename)

tags = ["SourceFile", "EXIF:CreateDate"]
with exiftool.ExifTool() as et:
    metadata = et.get_tags_batch(tags, files)
for d in metadata:
	#print(d["SourceFile"] + " " + d["EXIF:CreateDate"])
	print d

