# -*- coding: utf-8 -*-

"""Client functions."""

import json
import logging
import requests
from copy import deepcopy

import utils

def _generate_config_payload(parser_config):
    """This method maps the parser configuration structure into a correct payload
    that has to be send to the server. This is done because of some naming mismatches
    between parser configuration variables and server payload parameters.

    """
    payload = deepcopy(parser_config)
    payload['parserName'] = payload.pop('name')
    return payload

def _compose_url(method, base_url=None):
    base_url = utils.CONSOLE_ARGS.get('url', base_url)
    if base_url is None:
        base_url = 'https://facebook.tracking.exposed/api/v1/snippet/'
    if not base_url.endswith('/'):
        base_url += '/'
    return base_url + str(method)

def get_snippets_info(parser_config):
    """Get information about available snippets."""
    url = _compose_url('status')
    payload = _generate_config_payload(parser_config)
    logging.info("Requesting info about available snippets...")
    resp = requests.post(url, data=payload)
    # Raise an exception if we get a 4XX client error or 5XX server error response
    resp.raise_for_status()
    logging.debug("Response: %s", resp.content)
    return json.loads(resp.text)

def get_snippets(parser_config):
    """
    Fetch snippets. Note: we can only fetch a limited amount of snippets, which
    is defined by the 'limit' value retrieved from `get_snippets_info`.

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
            "htmlId": "<hash of html snippet>"
          },
        ]

    """
    logging.info("Fetching snippets...")
    url = _compose_url('content')
    payload = _generate_config_payload(parser_config)
    resp = requests.post(url, data=payload)

    return json.loads(resp.text)

def commit_result(parser_config, new_meta, snippet):
    """Commit new metadata obtained by executing a parser over the snippet."""
    # logging.debug("Committing new metadata for snippet %s", snippet['id'])
    url = _compose_url('result')
    payload = {
        'htmlId': snippet['id'],
        'parserKey': parser_config['key'],
        'metadata': new_meta,
        'fields': new_meta.keys(),
        'parserName': parser_config['name']
    }
    return {'this is a result': True}
    # TODO: Uncomment to make it work
    # return requests.post(url, data=payload)
