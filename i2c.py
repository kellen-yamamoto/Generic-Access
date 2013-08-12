#!/usr/bin/python

import sys, traceback, getopt
from abstracts.i2c_lib import i2c_lib
handle = i2c_lib()

def usage() :
    print ''
    print 'Usage: ', sys.argv[0], ' -[agrwdu]'
    print '   -a: Physical address of I2C device'
    print '   -g: Register address of I2C device'
    print '   -r: Number of bytes to read'
    print '   -w: data to write, comma separated'
    print '   -s: Scan bus for devices, no arguments'
    print '   -u: Force bus to unlock, no arguments'
    print ''
    sys.exit(0)

def main() :
    try :
        opts, args = getopt.getopt(sys.argv[1:], 'a:g:r:w:su')
    except getopt.GetoptError, err:
        print str(err)
        usage()
    addr = None
    reg = None
    rw = None
    data = None
    scan = None
    unlock = None
    for o, a in opts :
        if o == '-a' :
            addr = a
        elif o == '-g' :
            reg = a
        elif o == '-r' :
            rw = a
        elif o == '-w' :
            rw = 0
            data = a
        elif o == '-s' :
            scan = 1
        elif o == '-u' :
            unlock = 1
        else :
            usage()


    if scan == 1 :
        print '     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f'
        i = 0
        j = 0
        while i < 128 :
            print '{:02x}'.format(i), ':',
            while j < 16 :
                if (i+j) < 3 :
                    print '  ',
                else :
                    ret = handle.i2ctest(str(i+j))
                    if ret > -6 :
                        print '{:02x}'.format((i+j)),
                    else :
                        print '--',
                j += 1
            print ''
            i += 16
            j = 0
    elif unlock == 1 :
        handle.i2creleaselock()
    elif (addr == None or reg == None or rw == None) :
        print 'Missing arguments'
        usage()
    else :
        ret = handle.i2cparse(addr, reg, rw, data)
        if rw == 0 :
            if ret < 0 :
                print 'Write error'
        else :
            print ret
    sys.exit(0)

if __name__ == "__main__" :
    try :
        main()
    except Exception, e:
        print 'Exception: '+str(e.__class__)+': '+str(e)
        traceback.print_exc()
        handle.i2creleaselock()
        sys.exit(0)
