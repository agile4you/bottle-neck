# -*- coding: utf-8 -*-
"""CBV for bottle.py application instances.

Provides a base class for creating class-based web handlers for bottle.py
application instances with application routing mechanism.
"""

__author__ = "Papavassileiou Vassilis"
__date__ = "2015-11-29"
__version__ = "0.1"
__all__ = ['BaseHandler', 'HandlerMeta', 'route_method', 'plugin_method']


import inspect
import six


DEFAULT_ROUTES = ("get", "put", "post", "delete", "patch", "options")

CORS_ROUTES = ("put", "post", "delete", "patch")

PLUGIN_SCOPE = (
    ('optional', 'plugins'),
    ('global', 'global_plugins')
)


class HandlerError(Exception):
    """Base module Exception class.
    """
    pass


class InvalidHTTPMethodError(HandlerError):
    """Raises for invalid HTTP method declaration.
    """
    pass


class HandlerPluginError(HandlerError):
    """Raises when a handler plugin error occurs.
    """
    pass


def plugin_method(*plugin_names):
    """Plugin Method decorator.
    Signs a web handler function with the plugins to be applied as attributes.

    Args:
        plugin_names (list): A list of plugin callable names

    Returns:
        A wrapped handler callable.

    Examples:
        >>> @plugin_method('json', 'bill')
        ... def method():
        ...     return "Hello!"
        ...
        >>> print method.json
        True
        >>> print method.bill
        True

    """
    def wrapper(callable_obj):
        for plugin_name in plugin_names:
            if not hasattr(callable_obj, plugin_name):
                setattr(callable_obj, plugin_name, True)
        return callable_obj
    return wrapper


def route_method(method_name, extra_part=False):
    """Custom handler routing decorator.
    Signs a web handler callable with the http method as attribute.

    Args:
        method_name (str): HTTP method name (i.e GET, POST)
        extra_part (bool): Indicates if wrapped callable name should be a part
                           of the actual endpoint.

    Returns:
        A wrapped handler callable.

    examples:
        >>> @route_method('GET')
        ... def method():
        ...     return "Hello!"
        ...
        >>> method.http_method
        'GET'
        >>> method.url_extra_part
        None
    """
    def wrapper(callable_obj):
        if method_name.lower() not in DEFAULT_ROUTES:
            raise InvalidHTTPMethodError(
                'Invalid http method in method: {}'.format(method_name)
            )

        callable_obj.http_method = method_name.upper()

        callable_obj.url_extra_part = callable_obj.__name__ if extra_part\
            else None

        return classmethod(callable_obj)
    return wrapper


class HandlerMeta(type):
    """BaseHandler metaclass

    Provides meta functionality for ensuring that `http_method` don't require
    an instance and test and that derived classes implements `Singleton`.
    """
    _instances = {}

    def __new__(mcs, name, bases, attrs):

        http_methods = [attr for attr in attrs if
                        attr.lower() in DEFAULT_ROUTES]

        for handler in http_methods:
            attrs[handler] = classmethod(attrs[handler])

        return super(HandlerMeta, mcs).__new__(mcs, name, bases, attrs)

    def __call__(cls, *args):
        """Enforce Singleton class initiation
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(
                HandlerMeta, cls
            ).__call__(*args)
        return cls._instances[cls]


@six.add_metaclass(HandlerMeta)
class BaseHandler(object):
    """Base Handler class for implementing Class-Based Web handler for bottle.

    Subclass `BaseHandler` in order to its API for application routing, and
    implement any of the known http method:

    Attributes:

        - base_endpoint (str): The handler endpoint prefix.
        - cors_enabled (bool): Indicates if CORS is enabled.
        - plugins (dict): A key/value mapping of available plugins.
        - global_plugins (dict): A key/value mapping default applying plugins.
    """

    base_endpoint = '/'
    cors_enabled = True
    plugins = dict()
    global_plugins = dict()

    @classmethod
    def add_plugin(cls, plugin_callables, scope='private'):
        """Register a new plugin in handler.
        """
        repo = getattr(cls, dict(PLUGIN_SCOPE)[scope])

        for plugin_callable in plugin_callables:

            if hasattr(plugin_callable, 'func_name'):
                repo[plugin_callable.func_name] = plugin_callable
            else:
                repo[plugin_callable.im_func.func_name] = plugin_callable

    @classmethod
    def register_app(cls, application):
        """Register class view in bottle application.
        """

        assert cls is not BaseHandler,\
            "Cant register a `BaseHandler` class instance"

        routes = cls._get_http_members()

        router = getattr(application, "route")

        for func_name, func_callable in routes:
            method_args = inspect.getargspec(func_callable)[0]
            method_args.remove('self')

            if hasattr(func_callable, 'http_method'):
                http_method = func_callable.http_method
                url_extra_part = func_callable.url_extra_part
            else:
                http_method = func_name
                url_extra_part = None

            applied_plugins = [pl for pl in cls.plugins
                               if hasattr(func_callable, pl)]

            for plugin in applied_plugins:
                try:
                    func_callable = cls.plugins[plugin](func_callable)
                except TypeError, error:
                    raise HandlerPluginError(error.args)

            for global_plugin in cls.global_plugins:
                func_callable = cls.global_plugins[global_plugin](
                    func_callable
                )

            router(
                cls._build_routes(method_args, url_extra_part),
                method=[http_method.upper()]
            )(func_callable)

        if cls.cors_enabled:
            options_data = {
                "handler": {"name": cls.__name__, "desc": cls.__doc__.strip()},
                "http_methods": [r[0] for r in routes]
            }

            router(
                cls.base_endpoint,
                method=["OPTIONS"]
            )(lambda: options_data)

            router(
                "{}/<url:re:.+>".format(cls.base_endpoint).replace("//", "/"),
                method=["OPTIONS"]
            )(lambda url: options_data)

    @classmethod
    def _build_routes(cls, method_args, url_extra_part=None):
        """Create bottle route for a handler http method."""

        prefix = '/{}'.format(url_extra_part) if url_extra_part else ''

        prefix += '/:' if method_args else ''

        endpoint = cls.base_endpoint + prefix + '/:'.join(method_args)

        return endpoint.replace("//", '/')

    @classmethod
    def _get_http_members(cls):
        """Filter all `http` specific method from handler class.
        """
        return [member for member in
                inspect.getmembers(cls, predicate=inspect.ismethod)
                if cls._check_http_member(member)]

    @staticmethod
    def _check_http_member(member):
        """Checks if a class method has HTTP info.
        """
        return member[0].lower() in DEFAULT_ROUTES or \
            hasattr(member[1], 'http_method')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
