# -*- coding: utf-8 -*-
"""Bottle.py middleware development utilities.

Provides a basic interface for applying a middleware to 'bottle.py' apps or web
services.
"""

from __future__ import absolute_import


__author__ = 'pav'
__date__ = '18-04-2015'
__all__ = ['BaseMiddleware', 'StripPathMiddleware']


from bottle_neck import __version__

version = tuple(map(int, __version__.split('.')))


class BaseMiddleware(object):
    """BaseMiddleware Abstract class. Provides an interface for creating
    middleware classes that act like proxy-wrappers to the actual bottle
    application instance.

    Subclass BaseMiddleware class and implement `__call__(self, e, h)`
    magic method in order to create an application transparent middleware


    Examples:
        >>> import bottle
        >>>
        ... class MyMiddle(BaseMiddleware):
        ...     def __call__(self, e, h):
        ...         print 'Hi from middleware'
        ...         self.app(e, h)
        ...
        >>> app = MyMiddle(bottle.Bottle())
        >>> print hasattr(app, 'route')
        True
        >>> class MyMw1(BaseMiddleware):
        ...     def __call__(self, e, h):
        ...         print 'Hi from middleware 1'
        ...         self.app(e, h)
        ...
        >>> class MyMw2(BaseMiddleware):
        ...     def __call__(self, e, h):
        ...         print 'Hi from middleware 2'
        ...         self.app(e, h)
        ...
        >>> app = MyMw2(MyMw1(bottle.Bottle()))
        >>> print hasattr(app, 'route')
        True
    """

    def __init__(self, app):
        self.app = app

    def __getattr__(self, attr):
        try:
            return getattr(self.app, attr)
        except AttributeError:  # pragma: no cover
            return None

    def __dir__(self):  # pragma: no cover
        return dir(self.app)

    def __call__(self, e, h):  # pragma: no cover
        raise NotImplementedError('Must implement __call__ method')


class StripPathMiddleware(BaseMiddleware):
    """Middleware class that handles url ending slashes.

    Development does not enforce URL dispatching with trailing slashes,
    but the end user has both kind of `variations` available.
    Straight copy/pasted from 'bottle.py' docs.
    """

    def __call__(self, e, h):  # pragma: no cover
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.app(e, h)


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
