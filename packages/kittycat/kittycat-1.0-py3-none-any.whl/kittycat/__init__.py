from guillotina import *

from guillotina.commands import command_runner
from guillotina.commands import MISSING_SETTINGS
MISSING_SETTINGS['jsapps']['+admin'] = 'kittycat:static/catherder'
