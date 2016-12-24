#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import parser_runner

def get_post_language(snippet):
    """Note: the `new_meta` keys need to be equal to those declared in
    `parsers-keys.json`.

    """
    result = 'new metadata value'
    # return {'postLanguage': result}
    return {'postType': result}

POST_LANGUAGE_CONFIG = {
    'name': 'postType',
    'parserName': 'postType',
    'requirements': {},
    'implementation': get_post_language,
    'since': "2016-11-13",
    'until': datetime.now().isoformat()
}

if __name__ == '__main__':
    parser_runner.run(POST_LANGUAGE_CONFIG)
