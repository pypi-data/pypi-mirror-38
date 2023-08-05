#This is necessary because some source files are needed in this case.

import os
import sys

def get_path():
    try:
        modpath = __file__
    except AttributeError:
        sys.exit('Module does not have __file__ defined.')
    
    # Turn pyc files into py files if we can
    if modpath.endswith('.pyc') and os.path.exists(modpath[:-1]):
        modpath = modpath[:-1]

    # Sort out symlinks
    modpath = os.path.realpath(modpath)
    modpath = os.path.dirname(modpath)
    modpath = modpath + '/'
    return modpath
