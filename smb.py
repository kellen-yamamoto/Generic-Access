#!/usr/bin/python

import os, sys, traceback, getopt
from abstracts.smb_lib import smb_lib
handle = smb_lib()

def usage() :
    print ''
    print 'Usage: ', sys.argv[0], ' -[acrweu]'
    print '   -a: SMBus address'
    print '   -c: Command byte'
    print '   -e: extended command byte'
    print '   -r: num of bytes to read'
    print '   -w: data to send, comma separated'
    print '   -u: force bus to unlock'
    print ''
    sys.exit(0)

def main() :
    try :
        opts, args, = getopt.getopt(sys.argv[1:], 'a:c:r:w:e:u')
    except getopt.GetoptError, err:
        print str(err)
        usage()

    addr = None
    cmd = None
    rw = None
    data = None
    length = None
    unlock = None
    extcmd = None

    for o, a in opts :
        if o == '-a' :
            addr = a
        elif o == '-c' :
            cmd = a
        elif o == '-r' :
            rw = 0
            length = a
        elif o == '-w' :
            rw = 1
            data = a
        elif o == '-u' :
            unlock = 1
        elif o == '-e' :
            extcmd = a
        else :
            usage()

    if unlock == 1 :
        handle.smbreleaselock()
    elif (addr == None or rw == None) :
        print 'Missing arguments'
        usage()
    else :
        ret = handle.smbparse(addr, cmd, rw, data, length, extcmd)
        if rw == 1 :
            if ret < 0 :
                print 'Write Error'
        else :
            print ret
    sys.exit(0)

if __name__ == "__main__" :
    try :
        main()
    except Exception, e:
        print 'Exception: '+str(e.__class__)+': '+str(e)
        traceback.print_exc()
        handle.smbreleaselock()
        sys.exit(0)
