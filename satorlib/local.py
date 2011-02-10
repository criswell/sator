import os
import sys
import signal

from satorlib import *

def local(config, root, argv):
    '''
    Local path
    '''
    handler = localhandler.LocalHandler(config, root)

    if not handler.autossh:
        print "autossh not found on system!"
        print "Please install autossh and try again..."
        sys.exit()

    # Check if there's already an autossh running for our connections
    if os.path.isfile(autossh_pidfile):
        # PID exists, verify it is running
        with open(autossh_pidfile, 'r') as f:
            autossh_pid = f.read().rstrip()

        if autossh_pid:
            if os.path.exist("/proc/%s" % autossh_pid):
                # Autossh verified as running
                autossh_running = True

    # Check for sub-commands
    if "shutdown" in argv:
        if autossh_running:
            # First, shut down the linkage with the remote connection
            # FIXME

            # Okay, let's shutdown the current autossh connection
            os.kill(autossh_pid, signal.SIGTERM)
    else:
        # The assumption here is we want to start a new connection
        if autossh_running:
            print "autossh is currently running with pid %s" % autossh_pid
            print "See 'help' for usage information"
            sys.exit()
        else:
            # Get our linkage information
            # FIXME

            # Now, run autossh
            # FIXME