from satorlib import *
import satorlib.remotehandler as remotehandler

def remote(config, root, argv):
    '''
    Remote path
    '''
    handler = remotehandler.RemoteHandler(config, root)

    # Check for sub-commands
    command = argv[0]
    if command == 'myport':
        # Obtain a port for a machine
        if len(argv) == 2:
            # myport accepts one and only one parameter
            host = argv[1]
            port = handler.setup_port_for_host(host)
            if port:
                print port
            else:
                print remote_error_code 
        else:
            print remote_error_code
