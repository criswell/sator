import os
import sys
import signal

from satorlib import *
import satorlib.localhandler as localhandler

def local(config, root, argv):
    '''
    Local path
    '''
    handler = localhandler.LocalHandler(config, root)

    if not handler.autossh:
        print "autossh not found on system!"
        print "Please install autossh and try again..."
        sys.exit()
    elif not handler.ssh:
        print "ssh not found on system!"
        print "Please install ssh and try again..."
        sys.exit()

    # Check for sub-commands
    command = argv[0]
    if command == 'ls':
        if len(handler.all_remote):
            print "(Machine ID)\t(Active)\t(PID)"
            for sysname in handler.all_remote:
                if handler.autossh_running[sysname]:
                    print "%s\tYES\t%s" % (sysname, handler.autossh_pids[sysname])
                else:
                    print "%s\tNO" % (sysname)
        else:
            print "No remote systems defined"
