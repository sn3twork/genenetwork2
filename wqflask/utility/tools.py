# Tools/paths finder resolves external paths from settings and/or environment
# variables
#
# Currently supported:
#
#   PYLMM_PATH finds the root of the git repository of the pylmm_gn2 tool 

import os
import sys
from wqflask import app


def get_setting(command_id,guess=None):
    """Resolve a setting from the environment or the global settings in
    app.config, with get_valid_path is a function checking whether the
    path points to an expected directory and returns the full path to
    the binary command

      guess = os.environ.get('HOME')+'/pylmm'
      get_setting('PYLMM_PATH',guess)

    first tries the environment variable in +id+, next gets the Flask
    app setting for the same +id+ and finally does an educated
    +guess+.

    In all, the environment overrides the others, next is the flask
    setting, then the guess. A valid path to the binary command is
    returned. If none is resolved an exception is thrown.

    Note that we do not use the system path. This is on purpose
    because it will mess up controlled (reproducible) deployment. The
    proper way is to either use the GNU Guix defaults as listed in
    etc/default_settings.py or override them yourself by creating a
    different settings.py file (or setting the environment).

    """
    def value(command):
        if command:
            sys.stderr.write("Found value "+command+"\n")
            return command
        else:
            return None
    
    # ---- Check whether environment exists
    sys.stderr.write("Looking for "+command_id+"\n")
    command = value(os.environ.get(command_id))
    if not command:
        # ---- Check whether setting exists in app
        command = value(app.config.get(command_id))
        if not command:
            command = value(guess)
            if not command:
                raise Exception(command_id+' path unknown or faulty (update settings.py?). '+command_id+' should point to the path')
    return command

def valid_bin(bin):
    if os.path.islink(bin) or os.path.isfile(bin):
        return bin
    return None

def valid_path(dir):
    if os.path.isdir(dir):
        return dir
    return None

def pylmm_command(guess=None):
    return valid_bin(get_setting("PYLMM_RUN",guess))

def gemma_command(guess=None):
    return valid_bin(get_setting("GEMMA_RUN",guess))

def plink_command(guess=None):
    return valid_bin(get_setting("PLINK_RUN",guess))

def flat_files(subdir=None):
    base = get_setting("GENENETWORK_FILES")
    if subdir:
        return valid_path(base+"/"+subdir)
    return valid_path(base)

def tempdir():
    return valid_path(get_setting("TEMPDIR","/tmp"))

TEMPDIR = tempdir()
