#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_post_type(snippet):
    result = 'new metadata value'
    # print({ 'myParserName': result })
    return { 'myParserName': result }

post_type_config = {
    'name': 'postType',
    'parserName': 'postType',
    'requirements': {},
    # 'requirements': { "postType" : "promoted" },
    'implementation': get_post_type,
    'since': "2016-12-21T20:00:00Z",
    'until': "2016-12-22T20:10:00Z" # Rendi dinamico (fino a time.now() ISO8601 DateTime)
    # 'since': "2016-12-17T20:00:00Z",
    # 'until': "2016-12-17T20:10:00Z" # Rendi dinamico (fino a time.now() ISO8601 DateTime)
}
