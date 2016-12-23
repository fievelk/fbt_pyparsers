import json

def import_parser_key(parser_config):
    extended_config = parser_config[:]
    parsers_keys = json.load(open('parsers-keys.json', 'r'))
    # TODO: gestire i fields! Servono a qualcosa?
    try:
        match = next((item for item in parsers_keys if item['name'] == extended_config['name']))
        extended_config.update({'key': match['key']})
    except StopIteration as e:
        logging.error('Your parser key was not found in parsers-keys.json')
        raise e

    return extended_config
