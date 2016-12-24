#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main runner for parsers"""

from __future__ import division

import logging
import signal

from parser_client import get_snippets_info, get_snippets, commit_result
from utils import import_parser_key, _parse_arguments, _signal_handler

def count_slots(snippets_info):
    """Count slots that have to be used in order to group requests.
    We allocate at least one slot.

    """
    available = int(snippets_info['available'])
    limit = int(snippets_info['limit'])
    slots = 1 if (available // limit == 0) else available // limit
    logging.debug("%d HTMLs, %d per request = %d requests",
                  snippets_info['available'], snippets_info['limit'], slots)
    return slots

# TODO: Check whether we need this step or we can directly iterate using just one config.
def iterate_on_slots(parser_config):
    """Iterate over slots and generate new config objects for parser. Each config
    contains a different value for the `index` key.

    """
    for i in range(parser_config['slots']):
        index = {'index': i}
        logging.debug(index)
        yield dict(parser_config, **index)

def extract_metadata(parser_config, snippet):
    """Apply the parser implementation over the snippet and return new metadata."""
    return parser_config['implementation'](snippet['html'])

def process_html_bulk(parser_config):
    """Retrieve and process each snippet, committing resulting metadata. """
    snippets = get_snippets(parser_config) # Max 300 snippets for each iteration
    for snippet in snippets:
        new_metadata = extract_metadata(parser_config, snippet)
        commit_result(parser_config, new_metadata, snippet)

def run(parser_config):
    """Run parser.

    Example for debugging:
        python my_parser.py -d

    """
    console_args = _parse_arguments()
    signal.signal(signal.SIGINT, _signal_handler)

    parser_config['repeat'] = console_args.repeat
    # parser_config['snippetConcurrency'] = console_args.snippetConcurrency
    # parser_config['delay'] = console_args.delay

    parser_config = import_parser_key(parser_config)
    snippets_info = get_snippets_info(parser_config)
    parser_config['slots'] = count_slots(snippets_info)

    # for i in range(parser_config['slots']):
    for parser_config in iterate_on_slots(parser_config):
        process_html_bulk(parser_config)
