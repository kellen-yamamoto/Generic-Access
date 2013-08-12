#!/usr/bin/python

import sys, traceback, getopt
from abstracts.mdio_lib import mdio_lib

def usage() :
    print ''
    print 'Usage: ', sys.argv[0], ' -[pcagrwu]'
    print '   -p: PHY address of mdio device'
    print '   -a: Device address if using clause 45'
    print '   -g: Register address'
    print '   -r: Read, no arguments'
    print '   -w: Write data'
    print '   -u: Force bus to unlock'
    print ''
    sys.exit(0)

def main() :
    try :
        opts, args = getopt.getopt(sys.argv[1:], 'p:a:g:rw:u')
    except getopt.GetoptError, err:
        print str(err)
        usage()
    phy = None
    addr = None
    reg = None
    rw = None
    data = None
    unlock = None

    for o, a in opts :
        if o == '-p' :
            phy = a
        elif o == '-a' :
            addr = a
        elif o == '-g' :
            reg = a
        elif o == '-r' :
            rw = 0
        elif o == '-w' :
            rw = 1
            data = a
        elif o == '-u' :
            unlock = 1
        else :
            usage()

    handle = mdio_lib()

    if unlock == 1 :
        handle.mdioreleaselock()
    elif (phy == None or reg == None or rw == None) :
        print 'Missing arguments'
        usage()
    else :
        ret = handle.mdioparse(phy, addr, reg, rw, data)
        if rw == 0 :
            print ret
    sys.exit(0)

if __name__ == "__main__" :
    try :
        main()
    except Exception, e:
        print 'Exception: '+str(e.__class__)+': '+str(e)
        traceback.print_exc()
        handle.mdioreleaselock()
        sys.exit(0)
