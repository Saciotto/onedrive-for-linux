import os
from pathlib import Path
from configparser import ConfigParser

CONFIG_FILE = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' /
                                  'share' / 'onedrive_for_linux')) / 'config.ini'


def set_default_profile(profile_id):
    config = ConfigParser()
    config.read(CONFIG_FILE)
    if not 'DEFAULT' in config:
        config['DEFAULT'] = {}
    config['DEFAULT']['profile'] = profile_id
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def get_default_profile():
    config = ConfigParser()
    config.read(CONFIG_FILE)
    if not 'DEFAULT' in config or not 'profile' in config['DEFAULT']:
        return ''
    return config['DEFAULT']['profile']
