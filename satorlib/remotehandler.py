import os
import pickle
from satorlib import *

class RemoteHandler(object):
    '''
    The class that handles the various remote requests.
    '''
    def __init__(self, config, root):
        self._config = config
        self._root = root
        self._dictfile = "%s/%s" (self._root, remote_dictfile)
        self.all_remotes = None
        if os.path.isfile(self._dictfile):
            with open(self._dictfile, 'r') as f:
                self.all_remotes = pickle.load(f)
