import os
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

    def get_port_from_remote(self, uri):
        '''
        uri = username@host:rport

        Given a username, host, and remote port, will attempt to connect to it
        and ask the remote sator system what port we should use. If rport is
        None, then we will not use any special port settings.

        If we return None, then it means an error occured.
        '''
        