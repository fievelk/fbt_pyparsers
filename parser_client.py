#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import requests

"""Client functions"""

def _compose_url(method):
    base_url = 'https://facebook.tracking.exposed/api/v1/snippet/'
    return base_url + str(method)

def get_available_snippets_info(parser_config):
    """Get information about available snippets."""
    logging.info("Requesting info about available snippets...")
    url = _compose_url('status')
    payload = parser_config
    resp = requests.post(url, data=payload)
    logging.debug("Payload: %s", payload)
    logging.debug("RESPONSE: %s", resp.content)
    result = json.loads(resp.text)

    return int(result['available']), int(result['limit'])

def get_snippets(parser_config):
    """
    Fetch snippets. Note: we can only fetch a limited amount of snippets, which
    is defined by the 'limit' value retrieved from `get_available_snippets_info`.

    Parameters
    ----------
    parser_config : dict
        A dictionary containing the parser configuration.

    Returns
    -------
    json
        A json object containing an array of snippets with the following structure:
        [
          {
            "html": "<html snippet>",
            "metadata-1": "<value>",
            "metadata-2": "<value>",
            "snippetId": "<hash of html snippet>"
          },
        ]

    """
    logging.info("Fetching snippets...")
    url = _compose_url('content')
    payload = parser_config
    resp = requests.post(url, data=payload)

    return json.loads(resp.text)

def commit_result(parser_config, new_meta, snippet):
    """Commit new metadata obtained by executing a parser over the snippet."""
    logging.debug("Committing new metadata for snippet %s", snippet['id'])
    url = _compose_url('result')
    payload = {
        'snippetId': snippet['id'],
        'parserKey': parser_config['key'],
        'metadata': new_meta,
        'fields': new_meta.keys(),
        'parserName': parser_config['name']
    }
    # TODO: Uncomment to make it work
    # resp = requests.post(url, data=payload)

    # return resp.status
    print('DONE')
