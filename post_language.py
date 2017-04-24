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

from pyquery import PyQuery as pq
from langdetect import detect_langs

import parser_runner
import utils

def get_post_language(snippet):
    """
    Note: the `new_meta` keys need to be equal to those declared in
    `parsers-keys.json`.

    Parameters
    ----------
    snippet : str
        A snippet.

    Returns
    -------
    dict
        A dictionary object containing the parser results:
       {
         'postLanguage': true | false, (depending on success)
         'titleLanguage': '<value>',
         'contentLanguage': '<value>',
       }

    """
    fail_result = {'postLanguage': False}

    content_text = snippet.get('text')
    if not content_text:
        return fail_result

    try:
        language_scores = detect_langs(content_text)
    except Exception as e:
        return fail_result

    return {
        'postLanguage': True,
        # 'language': most_rated_language,
        'language_scores': language_scores
    }

POST_LANGUAGE_CONFIG = {
    # 'name': 'postLanguage',
    'name': 'postType', # This is just an example that has to be changed
    'requirements': {"feedText": True}, # Only use snippets for which text has been extracted
    'implementation': get_post_language,
    'since': "2017-04-24T12:00",
    'until': datetime.now().isoformat()
}

def start(arguments=None):
    """Start the parser."""
    if arguments is None:
        arguments = utils.configure_settings()
    parser_runner.run(arguments, POST_LANGUAGE_CONFIG)

if __name__ == '__main__':
    start(utils.configure_settings())
