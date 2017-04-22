# -*- coding: utf-8 -*-

"""Client functions."""

import json
import logging
from copy import deepcopy

import requests

import utils

def _generate_config_payload(parser_config):
    """
    Map the parser configuration structure into a correct payload that has to be
    sent to the server. This is done because of some naming mismatches between
    parser configuration variables and server payload parameters.

    """
    payload = deepcopy(parser_config)
    payload['parserName'] = payload.pop('name')

    return payload

def _compose_url(method, base_url=None):
    """
    Compose the destination URL using `base_url` and `method` strings. If
    base_url has not been explicitly specified, use the value provided from
    command-line. If that is not available either, use FTB default value.

    """
    if base_url is None:
        console_url = utils.CONSOLE_ARGS.get('url')
        base_url = console_url if console_url else 'https://facebook.tracking.exposed'
    base_url.rstrip('/')

    return '/'.join([base_url, 'api', 'v1', 'snippet', str(method)])

def get_snippets(parser_config):
    """
    Fetch snippets. Note: we can only fetch a limited amount of snippets
    depending on `since` and `until` fields defined in `parser_config`.

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

    try:
        snippets = json.loads(resp.text)
        if not snippets:
            logging.info("No snippets available!")
        return snippets
    except ValueError:
        logging.info("No snippets available!")
        return []

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
