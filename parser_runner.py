# -*- coding: utf-8 -*-

"""Main runner for parsers"""

from __future__ import division
import logging

import parser_client
import utils

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

def extract_metadata(parser_config, snippet):
    """Apply the parser over the snippet and return new metadata."""
    return parser_config['implementation'](snippet)

def process_html_bulk(parser_config):
    """Retrieve and process each snippet, committing resulting metadata."""
    snippets = parser_client.get_snippets(parser_config) # Max 300 snippets for each iteration
    for snippet in snippets:
        new_metadata = extract_metadata(parser_config, snippet)
        parser_client.commit_result(parser_config, new_metadata, snippet)

def run(arguments, parser_config):
    """Run parser."""
    parser_config['repeat'] = arguments['repeat']
    parser_config = utils.import_parser_key(parser_config)
    snippets_info = parser_client.get_snippets_info(parser_config)
    parser_config['slots'] = count_slots(snippets_info)

    for i in range(parser_config['slots']):
        logging.debug("Processing slot #%d", i+1)
        process_html_bulk(parser_config)
