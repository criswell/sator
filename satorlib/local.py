import os
import sys

from satorlib import *

def local(config, argv):
    '''
    Local path
    '''
    # First, find the autossh binary
    autossh = None
    for path in __search_paths:
        if os.path.isfile("%s/autossh" % path):
            autossh = "%s/autossh" % path
            break

    if not autossh:
        print "autossh not found on system!"
        print "Please install autossh and try again..."
        sys.exit()
