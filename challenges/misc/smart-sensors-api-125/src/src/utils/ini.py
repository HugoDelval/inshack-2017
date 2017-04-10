#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

import configparser
import os

_CONFIG_ = None

# ------------------------------------------------------------------------------------------
#                               EXTERN FUNCTIONS
# ------------------------------------------------------------------------------------------


def init_config(filename):
    """
        Initializes configuration loading it from INI file
    """
    global _CONFIG_
    ok = False
    if not _CONFIG_:
        _CONFIG_ = configparser.ConfigParser()
        if len(_CONFIG_.read(filename, encoding='utf-8')) > 0:
            print('Configuration file {0} successfully loaded !'.format(filename))
            ok = True
        else:
            print("Configuration file {0} can't be loaded !".format(filename))
    else:
        print('Configuration file has already been loaded !')
    return ok


def getenv(env_var, default=None):
    """
        Returns a configuration value from an environnement variable
    """
    return os.getenv(env_var, default)


def config(section, option, env_var=None, default=None, boolean=False):
    """
        Tries to retrieve configuration from environement vriable if not None and 
        then search INI file for the config finally return default value if the first
        two operations failed
    """
    res = None
    # try to search for environement var if not None
    if env_var:
        res = getenv(env_var)
    # then search in INI config if env var not found
    if not res:
        if _CONFIG_:
            if section in _CONFIG_.sections():
                if option in _CONFIG_[section]:
                    if boolean:
                        res = _CONFIG_[section].getboolean(option)
                    else:
                        res = _CONFIG_[section][option]
                else:
                    print("Missing option {0} in section {1} in configuration file !".format(option, section))
                    if default:
                        print("Using default configuration value: {0}".format(default))
                        res = default
            else:
                print("Missing section {0} in configuration file".format(section))
                if default:
                    print("Using default configuration value: {0}".format(default))
                    res = default
        else:
            print("Configuration file must be loaded to use config(section, option) function ! Call init_config(filename) before !")
            if default:
                print("Using default configuration value: {0}".format(default))
                res = default
    # finally return res
    return res
