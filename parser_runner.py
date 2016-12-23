#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main runner for parsers"""

from __future__ import division

import argparse
import json
import logging
import signal
import sys

from post_type_parser import post_type_config
from parser_client import get_available_snippets_info, get_snippets, commit_result

def run_parser(parser_config):
    """Run parser"""
    available, limit = get_available_snippets_info(parser_config)
    logging.info("Available snippets: %s", available)

    # Before submitting our new metadata, we have to enrich our parser configuration
    # with its key. This is passed to the server to check that the parser has
    # been authenticated and authorized.
    # NOTE: we could do this in def __init__() if we make MyParser a class
    parsers_keys = json.load(open('parsers-keys.json', 'r'))
    # TODO: gestire i fields! Servono a qualcosa?
    try:
        match = next((item for item in parsers_keys if item['name'] == parser_config['name']))
        parser_config.update({'key': match['key']})
    except StopIteration as e:
        logging.error('Your parser key was not found in parsers-keys.json')
        raise e

    if available == 0:
        logging.info("There are no available snippets to be parsed by %s parser.",
                      parser_config['name'])
        exit(0)

    slots = 1 if (available // limit == 0) else available // limit # We'll need at least one slot
    logging.debug("%d HTMLs, %d per request = %d requests",
                  available, limit, slots)
    for i in range(slots):
        parser_config.update({'index': i})
        snippets = get_snippets(parser_config) # Max: 300 snippets for each iteration
        for snippet in snippets:
            new_meta = parser_config['implementation'](snippet['html'])
            commit_result(parser_config, new_meta, snippet)


# ---------------------------------------------------------------------------- #
# Entry point: logging etc.
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
    args = parser.parse_args()
    _configure_logger(args.loglevel)

def main():
    """Main function."""
    signal.signal(signal.SIGINT, _signal_handler)
    run_parser(post_type_config)

if __name__ == '__main__':
    _parse_arguments()
    main()
