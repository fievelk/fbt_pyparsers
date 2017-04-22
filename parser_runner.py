# -*- coding: utf-8 -*-

"""Main runner for parsers"""

from __future__ import division
import logging

import parser_client
import utils

def extract_metadata(parser_config, snippet):
    """Apply the parser over the snippet and return new metadata."""
    return parser_config['implementation'](snippet)

def run(arguments, parser_config):
    """Run parser."""
    parser_config['repeat'] = arguments['repeat']
    parser_config = utils.import_parser_key(parser_config)
    snippets = parser_client.get_snippets(parser_config)

    for i, snippet in enumerate(snippets):
        logging.debug("Processing snippet #%d", i+1)
        new_metadata = extract_metadata(parser_config, snippet)
        parser_client.commit_result(parser_config, new_metadata, snippet)
