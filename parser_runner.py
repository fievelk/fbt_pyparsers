#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main runner for parsers"""

from __future__ import division

import argparse
import logging
import signal
import sys

from post_type_parser import post_type_config
from parser_client import get_available_snippets_info, get_snippets, commit_result
from utils import import_parser_key

def run_parser(parser_config):
    """Run parser"""
    available, limit = get_available_snippets_info(parser_config)
    logging.info("Available snippets: %s", available)

    # Enrich parser configuration with its key. This is used by the server to
    # check that the parser is authorized.
    parser_config = import_parser_key(parser_config)

    if available == 0:
        logging.info("There are no available snippets to be parsed by %s parser.",
                      parser_config['name'])
        sys.exit(0)

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
