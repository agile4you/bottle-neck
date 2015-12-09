# -*- coding: utf-8 -*-
"""Bottle.py API development utilities.

Provides some extra functionality for developing web API's with `bottle.py`.
"""

__author__ = 'pav'
__date__ = '2015-2-3'
__version__ = '0.1'
__all__ = ['cors_enable_hook', 'json_validator']


import bottle


def cors_enable_hook():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Headers'] = \
        'Authorization, Credentials, X-Requested-With, Content-Type'
    bottle.response.headers['Access-Control-Allow-Methods'] = \
        'GET, PUT, POST, OPTIONS, DELETE'


def strip_path_hook():
    """Ignore trailing slashes.
    """
    bottle.request.environ['PATH_INFO'] = \
        bottle.request.environ['PATH_INFO'].rstrip('/')
