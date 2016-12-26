#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility functions for parsers."""

import argparse
import json
import logging
import signal
import sys
from copy import deepcopy

# Console arguments are made available to the other modules
CONSOLE_ARGS = None

def import_parser_key(parser_config):
    """
    Enrich the parser configuration with its key. This is used by the server to
    check whether the parser can be authorized or not.

    """
    extended_config = deepcopy(parser_config)
    parsers_keys = json.load(open('parsers-keys.json', 'r'))
    try:
        match = next((item for item in parsers_keys if item['name'] == extended_config['name']))
        extended_config.update({'key': match['key']})
    except StopIteration as exception:
        logging.error('Your parser key was not found in parsers-keys.json')
        raise exception

    return set_requirements(extended_config)

def set_requirements(parser_config):
    """Set `requirements` in parser configuration."""
    parser_config = deepcopy(parser_config)
    repeat_flag = parser_config.get('repeat')
    if repeat_flag in [None, '']:
        pass
    elif isinstance(repeat_flag, str) and repeat_flag.lower() in ['true', 'false']:
        parser_config['requirements'] = {parser_config['name']: repeat_flag}
    else:
        raise WrongRequirementsException("parser_config['repeat'] should be a \
              ['true'|'false'] string.")

    return parser_config

# ---------------------------------------------------------------------------- #
# Exception handling
# ---------------------------------------------------------------------------- #

class WrongRequirementsException(TypeError):
    """Exception to be used when a wrong `requirements` parameter is provided."""
    pass

# ---------------------------------------------------------------------------- #
# Logging and command-line arguments.
# ---------------------------------------------------------------------------- #

def _signal_handler(signum, frame):
    """Handle CTRL-C signal to stop execution."""
    print('\nExiting!')
    sys.exit(0)

def _configure_logger(loglevel):
    """Configure logging levels."""
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.DEBUG)
    logging.basicConfig(level=loglevel)

def _parse_arguments():
    """Parse arguments provided from command-line and return them as a dictionary."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        help="Activates debug mode",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Activates verbose mode",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    parser.add_argument(
        '-r', '--repeat',
        help="Repeat flag",
        action="store", dest="repeat",
        default=None
    )
    parser.add_argument(
        '-u', '--url',
        help="Set base URL for API requests",
        action="store", dest="url",
        default=None
    )

    return vars(parser.parse_args())

def configure_settings():
    """Configure command-line arguments, logging levels and interruption signal.
    Return a dictionary of provided command-line arguments.

    """
    global CONSOLE_ARGS
    CONSOLE_ARGS = _parse_arguments()
    _configure_logger(CONSOLE_ARGS['loglevel'])
    signal.signal(signal.SIGINT, _signal_handler)

    return CONSOLE_ARGS
