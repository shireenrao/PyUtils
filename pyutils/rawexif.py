#!/usr/bin/env python

from struct import *

recognised_tags = { 
    0x0100 : 'imageWidth',
    0x0101 : 'imageLength',
    0x0102 : 'bitsPerSample',
    0x0103 : 'compression',
    0x010f : 'make',    
    0x0110 : 'model',
    0x0111 : 'stripOffset',
    0x0112 : 'orientation', 
    0x0117 : 'stripByteCounts',
    0x011a : 'xResolution',
    0x011b : 'yResolution',
    0x0128 : 'resolutionUnit',
    0x0132 : 'dateTime',
    0x8769 : 'EXIF',
    0x8825 : 'GPS data'};

def GetHeaderFromCR2( buffer ):
    # Unpack the header into a tuple
    header = unpack_from('HHLHBBL', buffer)
    """
    print "\nbyte_order = 0x%04X"%header[0]
    print "tiff_magic_word = %d"%header[1]
    print "tiff_offset = 0x%08X"%header[2]
    print "cr2_magic_word = %d"%header[3]
    print "cr2_major_version = %d"%header[4]
    print "cr2_minor_version = %d"%header[5]
    print "raw_ifd_offset = 0x%08X\n"%header[6]
    """
    return header

def FindDateTimeOffsetFromCR2( buffer, ifd_offset, endian_flag ):
    # Read the number of entries in IFD #0
    (num_of_entries,) = unpack_from(endian_flag+'H', buffer, ifd_offset)
    #print "Image File Directory #0 contains %d entries\n"%num_of_entries

    # Work out where the date time is stored
    datetime_offset = -1

    # Go through all the entries looking for the datetime field
    #print " id  | type |  number  |  value   "
    for entry_num in range(0,num_of_entries):

        # Grab this IFD entry
        (tag_id, tag_type, num_of_value, value) = unpack_from(endian_flag+'HHLL', buffer, ifd_offset+2+entry_num*12)

        # Print out the entry for information
        #print "%04X | %04X | %08X | %08X "%(tag_id, tag_type, num_of_value, value),
        #if tag_id in recognised_tags:
        #    print recognised_tags[tag_id]

        # If this is the datetime one we're looking for, make a note of the offset
        if tag_id == 0x0132:
            assert tag_type == 2
            assert num_of_value == 20
            datetime_offset = value

    return datetime_offset

if __name__ == '__main__':
    with open("IMG_0740.CR2", "rb") as f:
        # read the first 1kb of the file should be enough to find the date/time
        buffer = f.read(1024) 

        # Grab the various parts of the header
        (byte_order, tiff_magic_word, tiff_offset, cr2_magic_word, cr2_major_version, cr2_minor_version, raw_ifd_offset) = GetHeaderFromCR2(buffer)

        # Set the endian flag
        endian_flag = '@'
        if byte_order == 0x4D4D:
            # motorola format
            endian_flag = '>'
        elif byte_order == 0x4949:
            # intel format
            endian_flag = '<'

        # Search for the datetime entry offset
        datetime_offset = FindDateTimeOffsetFromCR2(buffer, 0x10, endian_flag)

        datetime_string = unpack_from(20*'s', buffer, datetime_offset)
        print "\nDatetime: "+"".join(datetime_string)+"\n"
