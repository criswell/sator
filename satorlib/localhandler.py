import os
import subprocess
from satorlib import *
from satorlib.ssh import SSH_Handler

class LocalHandler(object):
    '''
    The class that handles the various interactions for local connections
    '''
    def __init__(self, config, root):
        self._config = config
        self._root = root
        self.autossh = None
        self.autossh_pidfile_base = "%s/%s" % (self._root, autossh_pidfile)
        self.autossh_pids = {}
        self.autossh_running = {}

        # First, find the autossh binary
        if self._config.C.has_option('local', 'autossh'):
            self.autossh = self._config.C.get('local', 'autossh')
        else:
            for path in search_paths:
                if os.path.isfile("%s/autossh" % path):
                    self.autossh = "%s/autossh" % path
                    break

        # Next, let's establish what is currently running
        self.all_remote = None
        remote_sys = self.get_remote_systems()
        if remote_sys:
            self.all_remote = {}
            for entries in remote_sys:
                (system, uri) = entries
                self.all_remote[system] = uri
                pid = self.check_running_pid(system)
                if pid:
                    self.autossh_pids[system] = pid
                    self.autossh_running[system] = True
                else:
                    self.autossh_running[system] = False

        self.ssh = SSH_Handler(self._config)
        if not self.ssh.ssh:
            self.ssh = None

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
        pidfile = self.get_pidfile(sysname)
        # Check if there's already an autossh running for our connections
        if os.path.isfile(pidfile):
            # PID exists, verify it is running
            with open(pidfile, 'r') as f:
                pid = f.read().rstrip()

            if pid:
                if os.path.exist("/proc/%s" % pid):
                    # Autossh verified as running
                    return pid
                else:
                    # It must be dead, let's nuke the PID file
                    os.remove(pidfile)
        return None

    def start(self, sysname):
        '''
        Given a system name, will attempt to start a connection with it.
        '''
        if self.autossh_running[sysname]:
            # Hmm, well, we're already running, so return success?
            return True

        # Start by connecting with the remote system and finding out our port
        port = None
        callback_port = '22'
        if self.ssh:
            port = self.ssh.get_port_from_remote(self.all_remote[sysname])
            if(self._config.C.has_option('callback_ports', sysname)):
                callback_port = self._config.C.get('callback_ports', sysname)

        # Now, launch autossh with the appropriate port
        if port:
            # First, check error codes
            if port == remote_error_code:
                print "General remote error!"
                return False
            elif port == remote_already_active:
                print "Remote connection claims active, but local autossh dead!"
                return False
            elif port == remote_port_range_exhausted:
                print "Remote port range exhausted!"
                return False
            else:
                # Alright, launch autossh
                if self._launch_autossh(sysname, port, callback_port):
                    return True
                print "Problem launching autossh!"
                return False
        else:
            # some error occured
            return False

    def _launch_autossh(self, sysname, port, callback_port='22'):
        '''
        Internal method, do not call externally!

        Launch the autossh binary once we've established it's ready to go.
        '''
        if self.autossh:
            cmd = []
            (username, host, rport) = SSH_Handler.uri_split(self.all_remote[sysname])
            cmd.append(self.autossh)

            cmd.append("-R %s:localhost:%s" % (port, callback_port))
            if rport:
                cmd.append("-p %s" % rport)
            cmd.append("%s@%s" % (username, host))
            # FIXME - Set up the env
            autossh_obj = subprocess.Popen(cmd)
        else:
            return False
