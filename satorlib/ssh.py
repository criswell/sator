import os

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
            for path in __search_paths:
                if os.path.isfile("%s/ssh" % path):
                    self.ssh = "%s/ssh" % path
                    break

