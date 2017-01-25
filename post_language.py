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
import json

from pyquery import PyQuery as pq

from cavnar_trenkle_min import CavnarTrenkleImpl
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

    # Check if the other parser correctly parsed text
    # TODO: remove this part (this is already implicit thanks to requirements)
    snippet = _get_user_content(snippet) # Remove
    content_text = snippet.get('postText')
    if not content_text:
        return fail_result

    # NOTE: This should be ideally done only once, not in each iteration
    model_file = 'model_cavnar_trenkle.json'
    model = _load_json_file(model_file)
    implementation = CavnarTrenkleImpl()

    language_scores = implementation.predict_language_scores(content_text, model, error_value=8000)

    return {
        'postLanguage': True,
        # 'language': most_rated_language,
        'language_scores': language_scores
    }

POST_LANGUAGE_CONFIG = {
    # 'name': 'postLanguage',
    'name': 'postType', # This is just an example that has to be changed
    'requirements': {},
    # 'requirements': {postText: true}, # Only use snippets for which text has been extracted
    'implementation': get_post_language,
    'since': "2016-11-13",
    'until': datetime.now().isoformat()
}

# TODO: delete!
def _get_user_content(snippet):
    d = pq(snippet['html'])
    if not d:
        # We failed processing the html content
        return snippet
    content = d('.userContent[id]')
    if not content:
        content = d('.userContent')
    content_text = content.text()
    if not content_text:
        return snippet

    snippet['postText'] = content_text
    return snippet

# TODO: move in utils
def _load_json_file(input_file):
    with open(input_file) as in_file:
        result = json.load(in_file)
    return result

def start(arguments=None):
    """Start the parser."""
    if arguments is None:
        arguments = utils.configure_settings()
    parser_runner.run(arguments, POST_LANGUAGE_CONFIG)

if __name__ == '__main__':
    start(utils.configure_settings())
