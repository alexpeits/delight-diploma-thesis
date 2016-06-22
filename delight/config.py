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
import os


# Locate and load config.ini
_CONF_FILENAME = 'config.ini'
_THIS_DIR = os.path.abspath(os.path.dirname(__file__))
_CONFIG = os.path.join(_THIS_DIR, os.pardir, _CONF_FILENAME)

config = SafeConfigParser()
config.read(_CONFIG)


class DBConfig(object):
    DB_URI = config.get('database', 'DB_URI')


class GUIConfig(object):
    SECRET_KEY = config.get('gui', 'SECRET_KEY')
    DEBUG = config.get('gui', 'DEBUG')
