# -*- coding: utf-8 -*-
"""Bottle.py routing development utilities.

Provides a basic routing mechanism for 'bottle.py' applications.

Module documentation
++++++++++++++++++++
"""

from collections import namedtuple
from handlers import HandlerMeta


__author__ = 'pav'
__date__ = '18-04-2015'
__version__ = '0.0.1'

__all__ = ('Router', )


class RouteException(Exception):
    """Raise when a routing error occurs.
    """
    pass


Route = namedtuple('Route', ('uri', 'methods', 'callable_obj'))


class Router(object):
    """Base Router class for bottle.py WSGI applications.
    """

    def __init__(self):
        self._routes = set()

    def add_route(self, uri='/', methods=None, callable_obj=None):
        self._routes.add(Route(uri=uri, methods=tuple(methods),
                               callable_obj=callable_obj))

    @property
    def routes(self):
        return self._routes

    def add_handler(self, handler_cls, entrypoint='/'):
        if HandlerMeta in handler_cls.__class__.__mro__:
            handler_cls.base_endpoint = entrypoint
            self._routes.add(handler_cls)
            return
        raise RouteException("Invalid handler instance.")

    def mount(self, app=None):
        for endpoint in self._routes:
            if isinstance(endpoint, Route):
                app.route(endpoint.uri, endpoint.methods)(
                    endpoint.callable_obj
                )
            else:
                endpoint.register_app(app)

    def __repr__(self):
        return 'Router object: total {} routes'.format(len(self._routes))

    def __iter__(self):
        for route in self._routes:
            yield route
