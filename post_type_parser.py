#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parser implementation using Python.
The following fields are required for the configuration constant:
    `name`: name of the parser,
    `requirements`: {},
    `implementation`: the parsing function,
    `since`: the date from which snippets to be parsed should be retrieved (ISO8601)
    `until`: the date until which snippets to be parsed should be retrieved (ISO8601)

Console usage example for debugging:
    python my_parser.py -d
"""

from datetime import datetime

import parser_runner
import utils

def get_post_language(snippet):
    """Note: the `new_meta` keys need to be equal to those declared in
    `parsers-keys.json`.

    """
    result = 'new metadata value'
    # return {'postLanguage': result}
    return {'postType': result}

POST_LANGUAGE_CONFIG = {
    'name': 'postType',
    # 'parserName': 'postType',
    'requirements': {},
    'implementation': get_post_language,
    'since': "2016-11-13",
    'until': datetime.now().isoformat()
}

def start():
    parser_runner.run(utils.CONSOLE_ARGS, POST_LANGUAGE_CONFIG)

if __name__ == '__main__':
    start()
