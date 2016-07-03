"""
Delight's configuration module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains some hardcoded settings that
are required for the system to run, but also reads
settings from the config.ini file in the top directory,
using the python built-in ConfigParser

:author: Alexandros Peitsinis

"""

from ConfigParser import SafeConfigParser
from ConfigParser import NoOptionError
import os

# Locate and load config.ini
_CONF_FILENAME = 'config.ini'
_THIS_DIR = os.path.abspath(os.path.dirname(__file__))
_CONFIG = os.path.join(_THIS_DIR, os.pardir, _CONF_FILENAME)

config = SafeConfigParser()
config.read(_CONFIG)

# this is exactly how python-decouple handles booleans
# https://github.com/henriquebastos/python-decouple
_BOOL = {'true': True, 'on': True, '1': True,
         'false': False, 'off': False, '0': False}

def cast_bool(section, option):
    opt = config.get(section, option).lower()
    if opt not in _BOOL:
        raise ValueError('Invalid value set for {} in config.'
                         .format(option))
    return _BOOL[opt]


##########
# global #
##########

try:
    TESTING = cast_bool('global', 'TESTING')
except NoOptionError:
    TESTING = False

GW_ADDR = config.get('global', 'GW_ADDR')
DL_HOST = config.get('global', 'DL_HOST')
DL_PORT = int(config.get('global', 'DL_PORT'))
DL_AUTH_KEY = config.get('global', 'DL_AUTH_KEY')

############
# database #
############

class DBConfig:
    if TESTING:
        DB_URI = config.get('database', 'DB_TEST_URI')
    else:
        DB_URI = config.get('database', 'DB_URI')

###############
# mqtt broker #
###############

class MQTTConfig:
    HOST = config.get('mqtt', 'HOST')
    PORT = config.get('mqtt', 'PORT')
    if TESTING:
        TOPIC_BASE = config.get('mqtt', 'TOPIC_TEST_BASE')
    else:
        TOPIC_BASE = config.get('mqtt', 'TOPIC_BASE')

###########
# web gui #
###########

class GUIConfig:
    SECRET_KEY = config.get('gui', 'SECRET_KEY')
    try:
        DEBUG = cast_bool('gui', 'DEBUG')
    except NoOptionError:
        DEBUG = False

    # not used by Flask class, but include host and port anyway
    HOST = config.get('gui', 'HOST')
    PORT = int(config.get('gui', 'PORT'))

