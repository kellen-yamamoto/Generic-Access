#!/usr/bin/python

import sys, traceback, getopt
from abstracts.spi_lib import spi_lib

def usage() :
    print ''
    print 'Usage: ', sys.argv[0], ' -[crwu]'
    print '   -c: SPI byte commands, comma separated'
    print '   -r: bytes to read'
    print '   -w: bytes to write, comma separated'
    print '   -u: force bus to unlock'
    print ''
    sys.exit(0)

def main() :
    try :
        opts, args = getopt.getopt(sys.argv[1:], 'c:r:w:u')
    except getopt.GetoptError, err:
        print str(err)
        usage()

    cmd = None
    rw = None
    data = None
    unlock = None

    for o, a in opts :
        if o == '-c' :
            cmd = a
        elif o == '-r' :
            rw = a
        elif o == '-w' :
            rw = 0
            data = a
        elif o == '-u' :
            unlock = 1
        else :
            usage()

    handle = spi_lib()

    if unlock == 1 :
        handle.spireleaselock()
    elif (cmd == None or rw == None) :
        print 'Missing arguments'
        usage()
    else :
        ret = handle.spiparse(cmd, rw, data)
        if rw > 0 :
            print ret
    sys.exit(0)

if __name__ == "__main__" :
    try :
        main()
    except Exception, e:
        print 'Exception: '+str(e.__class__)+': '+str(e)
        traceback.print_exc()
        sys.exit(0)
