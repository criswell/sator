import os
import subprocess
from satorlib import *

class SSH_Handler(object):
    '''
    The wrapping class for the SSH portal
    '''
    def __init__(self, config):
        self.ssh = None
        self._config = config

        if self._config.C.has_option('global', 'ssh'):
            self.ssh = self._config.C.has_option('global', 'ssh')
        else:
            for path in search_paths:
                if os.path.isfile("%s/ssh" % path):
                    self.ssh = "%s/ssh" % path
                    break

    def uri_split(self, uri):
        '''
        Given a uri of the format "username@host:port" will return a tuple with
        each item split into its own element.
        '''
        (username, hostport) = uri.split('@')

        hp = hostport.split(':')
        host = None
        port = None

        if len(hp) > 1:
            host = hp[0]
            port = hp[1]
        else:
            host = hp[0]

        return (username, host, port)

    def _ssh_command(self, uri, command):
        '''
        Internal function, should not be called externally!

        Takes a URI and a command, and calls a remote sator install with it.
        Returns the output or None on failure.
        '''
        if self.ssh:
            (username, host, rport) = self.uri_split(uri)
            cmd = []
            cmd.append(self.ssh)
            if rport:
                cmd.append("-p %s" % rport)
            cmd.append("%s@%s" % (username, host))

            cmd.append(command)

            try:
                ssh_obj = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                output = ssh_obj.stdout.readlines()
                ssh_obj.stdout.close()
                output = [s.rstrip() for s in output]
                return output
            except:
                return None
        else:
            return None

    def get_port_from_remote(self, uri):
        '''
        uri = username@host:rport

        Given a username, host, and remote port, will attempt to connect to it
        and ask the remote sator system what port we should use. If rport is
        None, then we will not use any special port settings.

        If we return None, then it means an error occured.
        '''
        return self._ssh_command(uri, "sator remote myport %s" % self._config.C.get('local', 'machine_id'))
