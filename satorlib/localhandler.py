import os
from satorlib import *

class LocalHandler(object):
    '''
    The class that handles the various interactions for local connections
    '''
    def __init__(self, config, root):
        self._config = config
        self._root = root
        self.autossh = None
        self.autossh_pidfile_base = "%s/%s" % (self._root, __autossh_pidfile)
        self.autossh_pids = {}
        self.autossh_running = {}

        # First, find the autossh binary
        if(self._config.C.has_option('local', 'autossh'):
            self.autossh = self._config.C.get('local', 'autossh')
        else:
            for path in __search_paths:
                if os.path.isfile("%s/autossh" % path):
                    self.autossh = "%s/autossh" % path
                    break

        # Next, let's establish what is currently running
        self.all_remote = get_remote_systems()
        if self.all_remote:
            for system in self.all_remote:
                pid = check_running_pid(system)
                if pid:
                    self.autossh_pids[system] = pid
                    self.autossh_running[system] = True
                else:
                    self.autossh_running[system] = False

    def get_remote_systems(self):
        '''
        Get a list of the remote systems, or None if it doesn't exist
        '''
        if self._config.C.has_section('remote_systems'):
            return self._config.C.items('remote_systems')
        else:
            return None

    def get_pidfile(self, sysname):
        '''
        Given a system name, will return the appropriate PID file for
        autossh.
        '''
        return "%s.%s" % (self.autossh_pidfile_base, sysname)

    def check_running_pid(self, sysname):
        '''
        Given a system name, will check if there's an associated
        autossh running for that system. If so, will return the PID for it.
        If not, will return None.
        '''
        pidfile = get_pidfile(sysname)
        # Check if there's already an autossh running for our connections
        if os.path.isfile(pidfile):
            # PID exists, verify it is running
            with open(pidfile, 'r') as f:
                pid = f.read().rstrip()

            if pid:
                if os.path.exist("/proc/%s" % pid):
                    # Autossh verified as running
                    return pid
        return None