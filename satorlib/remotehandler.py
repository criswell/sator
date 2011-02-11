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

    def _get_free_port(self):
        '''
        Internal function, do not call!

        Returns a free port for use.
        '''
        pass # FIXME TODO

    def _save_remotes(self):
        '''
        Internal function, do not call!

        Saves the remotes data
        '''
        pass # FIXME TODO

    def setup_port_for_host(self, host):
        '''
        Given a host id, return and reserve a unique port for that host
        '''
        if self.all_remotes:
            if self.all_remotes.has_key(host):
                # Hmm, we already seem to have a reservation for this host
                if self.all_remotes[host].active:
                    # ...and we're supposedly already active, this is fubar?
                    return remote_already_active
                else:
                    # Okay, we're inactive, let's just activate it then
                    if self.all_remotes[host].port == None:
                        # Alright, this is embarassing, make a new port
                        self.all_remotes[host].port = self._get_free_port()

                    if self.all_remotes[host].port:
                        self.all_remotes[host].active = True

                    self._save_remotes()
                    return self.all_remotes[host].port
            else:
                # Okay, host is new to us
                remoteEntry = RemoteDefinition()
                remoteEntry.port = self._get_free_port()
                if remoteEntry.port:
                    remoteEntry.active = True
                self.all_remotes[host] = remoteEntry
                self._save_remotes()
                return self.remoteEntry.port
        else:
            # Hey! You're the first!
            self.all_remotes = {}
            remoteEntry = RemoteDefinition()
            remoteEntry.port = self._get_free_port()
            if remoteEntry.port:
                remoteEntry.active = True
            self.all_remotes[host] = remoteEntry
            self._save_remotes()
            return self.remoteEntry.port
