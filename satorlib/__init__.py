# Search paths
search_paths = [
    "/bin",
    "/usr/bin",
    "/usr/local/bin",
]

__version__ = '0.0.1'

autossh_pidfile = "autossh.pid"

# Our universal error code is -1
remote_error_code = '-1'

# If we attempt to make a connection with a system that is already active, this
# is the error code we get back
remote_already_active = '-10'

remote_dictfile = "remotes.dict"

class RemoteDefinition(object):
    def __init__(self):
        self.port = None
        self.active = False
