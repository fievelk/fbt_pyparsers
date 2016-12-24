#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility functions for parsers."""

import argparse
import json
import logging
import sys

from copy import deepcopy

def import_parser_key(parser_config):
    """
    Enrich parser configuration with its key. This is used by the server to check
    that the parser is authorized.

    """
    extended_config = deepcopy(parser_config)
    parsers_keys = json.load(open('parsers-keys.json', 'r'))
    try:
        match = next((item for item in parsers_keys if item['name'] == extended_config['name']))
        extended_config.update({'key': match['key']})
    except StopIteration as exception:
        logging.error('Your parser key was not found in parsers-keys.json')
        raise exception

    return extended_config

# ---------------------------------------------------------------------------- #
# Logging etc.
# ---------------------------------------------------------------------------- #

def _signal_handler(signum, frame):
    """Handle CTRL-C signal to stop execution."""
    print('\nExiting!')
    sys.exit(0)

def _configure_logger(loglevel):
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.DEBUG)
    logging.basicConfig(level=loglevel)

def _parse_arguments():
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
        help="Repeat",
        action="store_const", dest="repeat", const=None,
        default=None
    )
    # parser.add_argument(
    #     '--snippetConcurrency',
    #     help="Snippet Concurrency",
    #     action="store_const", dest="snippetConcurrency", const=None,
    #     default=5
    # )
    # parser.add_argument(
    #     '--delay',
    #     help="Delay",
    #     action="store_const", dest="delay", const=None,
    #     default=200
    # )
    args = parser.parse_args()
    _configure_logger(args.loglevel)
    return args
