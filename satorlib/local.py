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
        # List the connection states
        if len(handler.all_remote):
            print "(Machine ID)\t(Active)\t(PID)"
            for entry in handler.all_remote:
                print handler.autossh_running
                if handler.autossh_running[entry[0]]:
                    print "%s\tYES\t%s" % (entry[0], handler.autossh_pids[entry[0]])
                else:
                    print "%s\tNO" % (entry[0])
        else:
            print "No remote systems defined"
    elif command == 'start':
        # Start the connections
        if len(argv) > 1:
            machine_ids = argv[1:]
        else:
            machine_ids = []
            for entry in handler.all_remote:
                machine_ids.append(entry[0])
        if len(machine_ids) > 1:
            for sysname in machine_ids:
                if handler.autossh_running[sysname]:
                    print "Connection '%s' already running! Skipping..." % sysname
                else:
                    if handler.start(sysname):
                        print "Connection '%s' started..." % sysname
                    else:
                        print "Problem establishing connection '%s'..." % sysname
        else:
            print "No remote systems defined"
