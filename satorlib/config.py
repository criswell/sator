try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import sys
import os
import time

class SatorConfig(object):
    '''
    Very basic config object for sator
    '''
    def __init__(self, root):
        # Weeee! Hardcoded hackery!
        self._config_filename = "satorrc"
        self._sator_root = root
        self.C = configparser.SafeConfigParser()
        self._load_config()

    def _load_config(self):
        '''
        Loads the configuration file, or creates a blank one if none exists
        '''
        user_config = "%s/%s" % (self._sator_root, self._config_filename)
        if os.path.isdir(self._sator_root):
            if os.path.isfile(user_config):
                # Attempt to load it
                try:
                    self.C.readfp(open(user_config))
                    # Check for needed sections and items
                    if(self.C.has_option('remote', 'port_range_start') &
                       self.C.has_option('remote', 'port_range_end') &
                       self.C.has_option('local', 'machine_id')):
                        pass
                    else:
                        self._backup_config()
                        self._create_config()
                except (configparser.MissingSectionHeaderError,
                        configparser.ParsingError):
                    self._backup_config(user_config)
                    self._create_config(user_config)
            else:
                # Okay, we just create it
                self._create_config(user_config)
        else:
            # need to create directory and config
            os.mkdir(self._sator_root)
            self._create_config(user_config)

    def _backup_config(self, user_config):
        '''
        Back up the existing config
        '''
        # Our config file is fubar, we'll nuke it after backing it up
        backup_config = "%s.backup-%i" % (user_config % int(time.time()))
        os.rename(user_config, backup_config)

    def _create_config(self, user_config):
        '''
        Creates a default config file
        '''
        if(not self.C.has_section('remote')):
            self.C.add_section('remote')

        if(not self.C.has_section('local')):
            self.C.add_section('local')

        if(not self.C.has_section('remote_systems')):
            self.C.add_section('remote_systems')

        self.C.set('remote', 'port_range_start', '19999')
        self.C.set('remote', 'port_range_end', '29999')

        self.C.set('local', 'machine_id', os.uname()[1])
        with open(user_config, 'wb') as configfile:
            self.C.write(configfile)
