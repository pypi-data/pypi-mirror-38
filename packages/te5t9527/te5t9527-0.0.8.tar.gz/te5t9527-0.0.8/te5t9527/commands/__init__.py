import os
import pkgutil
from importlib import import_module

COMMANDS = 'commands'
COMMAND_DIR = os.path.dirname(os.path.abspath(__file__))

def get_plugins():
    plugins = []

    for _, name, ispkg in pkgutil.iter_modules([COMMAND_DIR]):
        if ispkg:
            module = import_module('te5t9527.{}.{}'.format(COMMANDS, name))
            plugins.append(module)

    return plugins
