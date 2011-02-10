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

    # Check for sub-commands
    #if "shutdown" in argv:
    #    if autossh_running:
            # First, shut down the linkage with the remote connection
            # FIXME

            # Okay, let's shutdown the current autossh connection
    #        os.kill(autossh_pid, signal.SIGTERM)
    #else:
        # The assumption here is we want to start a new connection
    #    if autossh_running:
    #        print "autossh is currently running with pid %s" % autossh_pid
    #        print "See 'help' for usage information"
    #        sys.exit()
    #    else:
            # Get our linkage information
            # FIXME

            # Now, run autossh
            # FIXME