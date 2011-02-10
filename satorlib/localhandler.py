import os
from satorlib import *

class LocalHandler(object):
    '''
    The class that handles the various interactions for local connections
    '''
    def __init__(self, config, root):
        self._config = config
        self._root = root
        # First, find the autossh binary
        self.autossh = None
        self.autossh_pidfile_base = "%s/%s" % (self._root, __autossh_pidfile)
        self.autossh_pid = None
        self.autossh_running = False

        if(self._config.C.has_option('local', 'autossh'):
            self.autossh = self._config.C.get('local', 'autossh')
        else:
            for path in __search_paths:
                if os.path.isfile("%s/autossh" % path):
                    self.autossh = "%s/autossh" % path
                    break
