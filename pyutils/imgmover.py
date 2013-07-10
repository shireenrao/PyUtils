#!/usr/bin/env python
'''
Created on Feb 11, 2013

@author: shireenrao
'''
import sys
import datetime
import os.path, time
import os, sys, errno
import shutil
import getopt
import glob
import logging
import time
import calendar

_version = 0.1
_source = ""
_target = ""

def version():
    """This Prints the version"""
    print "imgmover.py: Version " + str(_version)

def usage():
    """This prints the usage."""
    print __doc__
    

def has_avi_file(filename):
    """For given thm filename, find corresponding avi file. Return true if found """
    retval=(False,'', '')
    dir_name = os.path.dirname(filename)
    file_name= os.path.basename(filename)
    f_name, f_ext = os.path.splitext(file_name)
    avi_file1 = os.path.join(dir_name, f_name + '.AVI')
    avi_file2 = os.path.join(dir_name, f_name + '.avi')
    if not os.path.isfile(avi_file1):
        if os.path.isfile(avi_file2):
            retval=(True,f_name+'.avi',avi_file2)
    else:
        retval=(True,f_name+'.AVI',avi_file1)
    return retval        

def main(argv):
    global log
    formats = ('jpg', 'thm', 'cr2', 'avi')
    log = logging.getLogger()
    ch  = logging.StreamHandler()
    
    localtime   = time.localtime()
    timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
    debug = True
    log_file = os.path.join(os.getcwd(),'imgmover.log.' + timeString)

    if os.path.exists(os.path.dirname(log_file)):
        fh = logging.FileHandler(log_file)
    else:
        raise "log directory does not exist (" + os.path.dirname(log_file) + ")"
        sys.exit(1)

    log.addHandler(ch)
    log.addHandler(fh)

    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    try:
        opts, args = getopt.getopt(argv, "hvs:t:", ["help", "version", "source=", "target="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    if not opts:
        version()
        usage()
        exit()

    _source = ""
    _target = ""

    for o, a in opts:
        if o in ("-h", "--help"):
            version()
            usage()
            exit()
        elif o in ("-v", "--version"):
            version()
            exit()
        elif o in ("-s","--source"):
            _source = a
        elif o in ("-t", "--target"):
            _target = a
        else:
            assert False, "unhandled option"

    if not _source:
        _source = os.getcwd()

    if not _target:
        print "No target location provided!, Where will I copy this?"
        usage()
        exit()

    if not os.path.exists(_source):
        print "Source " + _source + " is not a directory!"
        usage()
        exit()

    if not os.path.exists(_target):
        print "Target " + _target + " is not a directory!"
        usage()
        exit()

    log.info("Processing and sorting " + _source + " to target " + _target)

    fileList = []
    for root, dirs, files in os.walk(_source):
        for name in files:
            filename = os.path.join(root,name)
            if filename.lower().endswith(formats):
                fileList.append(filename)

#    problems_loc = os.path.join(_target,"exif_problems")
#    try:
#        os.makedirs(problems_loc)
#    except OSError as exc:
#        if exc.errno == errno.EEXIST:
#            pass
#        else: raise
    to_be_processed = len(fileList)
    log.info ("images to be processed -> " + str(to_be_processed))

    processCount = 0
    nocreatedateCount = 0
    copyCount = 0
    skipCount = 0
    exceptionCount = 0
    has_avi = False
    for file in fileList:
        processCount = processCount + 1
        filename = os.path.basename(file)
        orig_path = os.path.dirname(file)
 #       if filename.lower().endswith('thm'):
 #           has_avi, avi_filename, avi_fullpath = has_avi_file(file)
        
        destpath = os.path.join(_target,orig_path[1:])
        try:
            os.makedirs(destpath)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else: raise
        dest_file = os.path.join(destpath,filename)
        
        try:
            if not os.path.isfile(dest_file):
                shutil.copy2(file, destpath)
                copyCount = copyCount + 1
                log.info( "(" + str(processCount) + "/" + str(to_be_processed) +") " + filename + " => " + destpath)
            else:
                skipCount = skipCount + 1
                log.error( "(" + str(processCount) + "/" + str(to_be_processed) +") " + file + " not copied as already exists in destination")
        except OSError as exc:
            exceptionCount = exceptionCount + 1
            log.critical( "(" + str(processCount) + "/" + str(to_be_processed) +") " + "Skipped " + file + " due to exception!")
            pass
#        if has_avi:
#            dest_avifile = os.path.join(destpath,avi_filename)
#            try:
#                if not os.path.isfile(dest_avifile):
#                    shutil.copy2(avi_fullpath, destpath)
#                    #copyCount = copyCount + 1
#                    log.info( "(" + str(processCount) + "/" + str(to_be_processed) +") " + avi_filename + " => " + destpath)
#                else:
#                    #skipCount = skipCount + 1
#                    log.error( "(" + str(processCount) + "/" + str(to_be_processed) +") " + dest_avifile + " not copied as already exists in destination")
#            except OSError as exc:
#                #exceptionCount = exceptionCount + 1
#                log.critical( "(" + str(processCount) + "/" + str(to_be_processed) +") " + "Skipped " + file + " due to exception!")
#                pass        

    log.info( "Copy Complete")
    log.info( "Files not copied because of no create date exif data: " + str(nocreatedateCount))
    log.info( "Files copied: " + str(copyCount))
    log.info( "Files skipped as they exist in destination: " + str(skipCount))
    log.info( "Exceptions while copying: " + str(exceptionCount))
        
if __name__ == '__main__':
    main(sys.argv[1:])
