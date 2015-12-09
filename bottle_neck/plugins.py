# -*- coding: utf-8 -*-
"""Bottle.py Application Plugin utilities.

Provides some base functionality for creating application-scope plugins for
`bottle.py`.
"""

__author__ = 'pav'
__date__ = '2015-12-9'
__version__ = '0.1'
__all__ = ['BasePlugin', 'WrapErrorPlugin']


import abc
import bottle
import six


@six.add_metaclass(abc.ABCMeta)
class BasePlugin(object):
    """'bottle.py' Plugin API version 2 interface.

    Provides a concrete Plugin Base class for creating bottle.py plugins
    """

    name = None

    api = 2

    def setup(self, app):
        """Make sure that other installed plugins don't affect the same
        keyword argument and check if metadata is available.
        """
        for other in app.plugins:
            if not isinstance(other, self.__class__):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError(
                    "Found other plugin registered as {} (non-unique keyword)."
                )

    @abc.abstractmethod
    def apply(self, callback, context):
        pass


class WrapErrorPlugin(BasePlugin):
    """Middleware class that catches `bottle.HTTPError` exceptions and returns
    default HTTP status code 200 using `bottle_neck.response.WSResponse` class
    for error wrapping.
    """

    def __init__(self, keyword, error_wrapper_cls):
        self.error_wrapper = error_wrapper_cls
        self.keyword = keyword

    def apply(self, callback, context):
        """Apply the HTTPError wrapper to the callback.
        """

        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except bottle.HTTPError, e:
                return self.error_wrapper.from_status(
                    status_line=e.status_line,
                    msg=e.body
                )

        return wrapper
