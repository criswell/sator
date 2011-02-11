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
        self._dictfile = "%s/%s" % (self._root, remote_dictfile)
        self.all_remotes = None
        if os.path.isfile(self._dictfile):
            with open(self._dictfile, 'r') as f:
                self.all_remotes = pickle.load(f)

    def _get_free_port(self):
        '''
        Internal function, do not call!

        Returns a free port for use.
        '''
        # First, get all the current ports in use
        ports_in_use = []
        for remotes in self.all_remotes.keys():
            if self.all_remotes[remotes].active and self.all_remotes[remotes].port:
                ports_in_use.append(self.all_remotes[remotes].port)

        # Next, start lowest, and find the first free port
        # NOTE - This may not be the most efficient, but we don't have to do
        # this very often (hopefully) so, unless it becomes a problem, we'll
        # not worry about it
        start = self._config.C.getint('remote', 'port_range_start')
        end = self._config.C.getint('remote', 'port_range_end')

        port = start
        while port < end:
            if not port in ports_in_use:
                return port
            port = port + 1

        # If we get here, then we have a problem
        return remote_port_range_exhausted

    def _save_remotes(self):
        '''
        Internal function, do not call!

        Saves the remotes data
        '''
        if self.all_remotes:
            with open(self._dictfile, 'w') as f:
                pickle.dump(self.all_remotes, f)

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
                return remoteEntry.port
        else:
            # Hey! You're the first!
            self.all_remotes = {}
            remoteEntry = RemoteDefinition()
            remoteEntry.port = self._get_free_port()
            if remoteEntry.port:
                remoteEntry.active = True
            self.all_remotes[host] = remoteEntry
            self._save_remotes()
            return remoteEntry.port
