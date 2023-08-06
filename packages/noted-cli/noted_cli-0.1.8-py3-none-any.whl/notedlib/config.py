import configparser
from os.path import join, dirname

config = configparser.SafeConfigParser()
config.read(join(dirname(__file__), 'default.ini'))
