#!/usr/bin/python

import sys, traceback
from abstracts.gpio_lib import gpio_lib
import getopt

def usage() :
    print ''
    print 'Usage: ', sys.argv[0], ' -[prw]'
    print '   -p: GPIO Pin number'
    print '   -r: Get value, no arguments'
    print '   -w: Value to write'
    print '   -u: Force bus to unlock, no arguments'
    print ''
    sys.exit(0)

def main() :
    try :
        opts, args = getopt.getopt(sys.argv[1:], 'p:rw:u')
    except getopt.GetoptError, err:
        print str(err)
        usage()

    gpio = None
    rw = None
    val = None
    unlock = None

    for o, a in opts :
        if o == '-p' :
            gpio = a
        elif o == '-r' :
            rw = 0
        elif o == '-w' :
            rw = 1
            val = a
        elif o == '-u' :
            unlock = 1
        else :
            usage()

    handle = gpio_lib()

    if unlock == 1 :
        handle.gpioreleaselock()
    elif (gpio == None or rw == None) :
        print 'Missing Arguments'
        usage()
    else :
        if rw == 1 :
            handle.gpiosetval(gpio, val)
        else :
            print handle.gpiogetval(gpio)

    sys.exit(0)

if __name__ == "__main__" :
    try :
        main()
    except Exception, e:
        print 'Exception: '+str(e.__class__)+': '+str(e)
        traceback.print_exc()
        sys.exit(0)
