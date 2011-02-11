# Search paths
search_paths = [
    "/bin",
    "/usr/bin",
    "/usr/local/bin",
]

__version__ = '0.0.1'

autossh_pidfile = "autossh.pid"

remote_dictfile = "remotes.dict"

class RemoteDefinition(object):
    self.name = ""
    self.port = None
    self.active = False
