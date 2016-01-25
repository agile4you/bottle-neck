# -*- coding: utf-8 -*-
"""Bottle.py routing development utilities.

Provides a basic routing mechanism for 'bottle.py' web services, with a simple
and unique interface for function-based / Class-based handlers.
"""

from __future__ import absolute_import

__author__ = 'pav'
__date__ = '18-04-2015'
__all__ = ['Router', 'RouteError']


from bottle_neck import __version__
from bottle_neck.cbv import HandlerMeta
import types

version = tuple(map(int, __version__.split('.')))


class RouteError(Exception):
    """Raise when a routing error occurs.
    """
    pass


class Route(object):
    """Base Route interface.

    It wraps function-based web handlers in order to provide a
    same interface for `bottle_neck.routing.Router` class functionality.
    """

    __slots__ = ('uri', 'methods', 'callable_obj')

    @classmethod
    def wrap_callable(cls, uri, methods, callable_obj):
        """Wraps function-based callable_obj into a `Route` instance, else
        proxies a `bottle_neck.handlers.BaseHandler` subclass instance.

        Args:
            uri (str):  The uri relative path.
            methods (tuple): A tuple of valid method strings.
            callable_obj (instance): The callable object.

        Returns:
            A route instance.

        Raises:
            RouteError for invalid callable object type.
        """
        if isinstance(callable_obj, HandlerMeta):
            callable_obj.base_endpoint = uri
            callable_obj.is_valid = True
            return callable_obj

        if isinstance(callable_obj, types.FunctionType):
            return cls(uri=uri, methods=methods, callable_obj=callable_obj)

        raise RouteError("Invalid handler type.")

    def __init__(self, uri, methods, callable_obj):
        self.uri = uri,
        self.methods = methods,
        self.callable_obj = callable_obj

    @property
    def is_valid(self):
        args = [self.uri, self.methods, self.callable_obj]
        return all([arg for arg in args])

    def register_app(self, app):
        """Register the route object to a `bottle.Bottle` app instance.

        Args:
            app (instance):

        Returns:
            Route instance (for chaining purposes)
        """
        app.route(self.uri, methods=self.methods)(self.callable_obj)

        return self


class Router(object):
    """Base Router class for bottle.py WSGI applications.
    """

    def __init__(self):
        self._routes = set()

    @property
    def routes(self):  # pragma: no cover
        return self._routes

    def register_handler(self, callable_obj, entrypoint, methods=('GET',)):
        """Register a handler callable to a specific route.

        Args:
            entrypoint (str): The uri relative path.
            methods (tuple): A tuple of valid method strings.
            callable_obj (callable): The callable object.

        Returns:
            The Router instance (for chaining purposes).

        Raises:
            RouteError, for missing routing params or invalid callable
            object type.
        """

        router_obj = Route.wrap_callable(
            uri=entrypoint,
            methods=methods,
            callable_obj=callable_obj
        )

        if router_obj.is_valid:
            self._routes.add(router_obj)
            return self
        
        raise RouteError(  # pragma: no cover
            "Missing params: methods: {} - entrypoint: {}".format(
                methods, entrypoint
            )
        )

    def mount(self, app=None):
        """Mounts all registered routes to a bottle.py application instance.

        Args:
            app (instance): A `bottle.Bottle()` application instance.

        Returns:
            The Router instance (for chaining purposes).
        """
        for endpoint in self._routes:
            endpoint.register_app(app)

        return self

    def __repr__(self):  # pragma: no cover
        return 'Router object: total {} routes'.format(len(self))

    def __len__(self):
        return len(self._routes)

    def __iter__(self):  # pragma: no cover
        for route in self._routes:
            yield route
