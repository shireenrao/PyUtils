#!/usr/bin/env python
'''
Created on Feb 10, 2013

@author: shireenrao
'''
import sys
import os.path
import time
import getopt
import logging


def has_thm_file(filename):
    """For given thm filename, find corresponding avi file.
    Return true if found """
    retval = (False, '', '')
    dir_name = os.path.dirname(filename)
    file_name = os.path.basename(filename)
    f_name, f_ext = os.path.splitext(file_name)
    thm_file1 = os.path.join(dir_name, f_name + '.THM')
    thm_file2 = os.path.join(dir_name, f_name + '.thm')
    if not os.path.isfile(thm_file1):
        if os.path.isfile(thm_file2):
            retval = (True, f_name + '.thm', thm_file2)
    else:
        retval = (True, f_name + '.THM', thm_file1)
    return retval


def main(argv):
    global log
    formats = ('jpg', 'thm', 'cr2', 'avi', 'mov')
    log = logging.getLogger()
    ch = logging.StreamHandler()

    localtime = time.localtime()
    timeString = time.strftime("%Y%m%d%H%M%S", localtime)
    debug = True
    log_file = os.path.join(os.getcwd(), 'logger.log.' + timeString)

    if os.path.exists(os.path.dirname(log_file)):
        fh = logging.FileHandler(log_file)
    else:
        raise "log directory does not exist (" \
            + os.path.dirname(log_file) + ")"
        sys.exit(1)

    log.addHandler(ch)
    log.addHandler(fh)

    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    try:
        opts, args = \
            getopt.getopt(argv, "hvs:", ["help", "version", "source="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        #usage()
        sys.exit(2)

    if not opts:
        #version()
        #usage()
        exit()

    _source = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            #version()
            #usage()
            exit()
        elif o in ("-v", "--version"):
            #version()
            exit()
        elif o in ("-s", "--source"):
            _source = a
        else:
            assert False, "unhandled option"

    if not _source:
        _source = os.getcwd()

    if not os.path.exists(_source):
        print "Source " + _source + " is not a directory!"
        #usage()
        exit()

    fileList = []
    avilist = []
    movlist = []
    jpglist = []
    cr2list = []
    thmlist = []

    for root, dirs, files in os.walk(_source):
        for name in files:
            filename = os.path.join(root, name)
            if filename.lower().endswith(formats):
                fileList.append(filename)
                if filename.lower().endswith('jpg'):
                    jpglist.append(filename)
                elif filename.lower().endswith('thm'):
                    thmlist.append(filename)
                elif filename.lower().endswith('avi'):
                    avilist.append(filename)
                elif filename.lower().endswith('mov'):
                    movlist.append(filename)
                elif filename.lower().endswith('cr2'):
                    cr2list.append(filename)

    to_be_processed = len(fileList)
    log.info("files found -> " + str(to_be_processed))
    jpgfile = len(jpglist)
    log.info("jpg found -> " + str(jpgfile))
    avifile = len(avilist)
    log.info("avi found -> " + str(avifile))
    movfile = len(movlist)
    log.info("mov found -> " + str(movfile))
    cr2file = len(cr2list)
    log.info("cr2 found -> " + str(cr2file))
    thmfile = len(thmlist)
    log.info("thm found -> " + str(thmfile))

    thmavilist = []
    justavilist = []
    for file in avilist:
        filename = os.path.basename(file)
        #orig_path = os.path.dirname(file)
        if filename.lower().endswith('avi'):
            has_thm, thm_filename, thm_fullpath = has_thm_file(file)
            if has_thm:
                thmavilist.append(file)
            else:
                justavilist.append(file)
    log.info("Total -> "
             + str(jpgfile + avifile + movfile + cr2file + thmfile))
    log.info("Special Video Report")
    avi_thm_count = len(thmavilist)
    log.info("avi + thm found -> " + str(avi_thm_count))
    just_avi_count = len(justavilist)
    log.info("Just avi found -> " + str(just_avi_count))


if __name__ == '__main__':
    main(sys.argv[1:])
