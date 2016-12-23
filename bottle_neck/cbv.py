# -*- coding: utf-8 -*-
"""CBV for bottle.py application instances.

Provides a base class for creating class-based web handlers for bottle.py
application instances with application routing mechanism.
"""

from __future__ import absolute_import

__author__ = "Papavassiliou Vassilis"
__date__ = "2015-11-29"
__all__ = ['BaseHandler', 'HandlerMeta', 'route_method', 'plugin_method',
           'HandlerError', 'HandlerHTTPMethodError', 'HandlerPluginError',
           'BaseHandlerPlugin']


from bottle_neck import __version__
import bottle
import functools
import inspect
import six
import re


version = tuple(map(int, __version__.split('.')))

DEFAULT_ROUTES = ("get", "put", "post", "delete", "patch", "options")

CORS_ROUTES = ("put", "post", "delete", "patch")

PLUGIN_SCOPE = (
    (False, 'plugins'),
    (True, 'global_plugins')
)


class HandlerError(Exception):
    """Base module Exception class.
    """
    pass


class HandlerHTTPMethodError(HandlerError):
    """Raises for invalid HTTP method declaration.
    """
    pass


class HandlerPluginError(HandlerError):
    """Raises when a handler plugin error occurs.
    """
    pass


class ClassPropertyDescriptor(object):
    """ClassProperty Descriptor class.

    Straight up stolen from stack overflow Implements class level property
    non-data descriptor.
    """

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, cls=None):
        if cls is None:  # pragma: no cover
            cls = type(obj)
        return self.fget.__get__(obj, cls)()


def classproperty(func):
    """classproperty decorator.
    Using this decorator a class can have a property. Necessary for properties
    that don't need instance initialization. Works exactly the same as a
    normal property.

    Examples:
        >>> class MyClass(object):
        ...     @classproperty
        ...     def my_prop(self):
        ...         return self.__name__ + ' class'
        ...
        >>> MyClass.my_prop
        'MyClass class'
    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


def cached_classproperty(fun):
    """A memorization decorator for class  properties.

    It implements the above `classproperty` decorator, with
    the difference that the function result is computed and attached
    to class as direct attribute. (Lazy loading and caching.)
    """
    @functools.wraps(fun)
    def get(cls):
        try:
            return cls.__cache[fun]
        except AttributeError:
            cls.__cache = {}
        except KeyError:  # pragma: no cover
            pass
        ret = cls.__cache[fun] = fun(cls)
        return ret
    return classproperty(get)


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
            raise HandlerHTTPMethodError(
                'Invalid http method in method: {}'.format(method_name)
            )

        callable_obj.http_method = method_name.upper()

        callable_obj.url_extra_part = callable_obj.__name__ if extra_part\
            else None

        return classmethod(callable_obj)
    return wrapper


class BaseHandlerPlugin(object):
    """
    """
    def __init__(self, callable_object, *args, **kwargs):  # pragma: no cover
        self._wrapped = callable_object
        self._args = args
        self._kwargs = kwargs
        self.__doc__ = callable_object.__doc__

    @cached_classproperty
    def func_name(self):
        cls_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', cls_name).lower()

    def apply(self, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Must Override `apply` method")

    def __call__(self, *args, **kwargs):  # pragma: no cover
        return self.apply(*args, **kwargs)


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

    Class attributes:
        base_endpoint (str): The handler endpoint prefix.
        cors_enabled (bool): Indicates if CORS is enabled.
        plugins (dict): A key/value mapping of available plugins.
        global_plugins (dict): A key/value mapping default applying plugins.
    """
    request = bottle.request
    response = bottle.response
    base_endpoint = '/'
    cors_enabled = True
    plugins = dict()
    global_plugins = dict()

    @classmethod
    def add_plugin(cls, plugin_callables, global_scope=False):
        """Register a new plugin in handler.

        Args:
            plugin_callables (list): A list of plugin callables.
            global_scope (bool): Indicates The scope of the plugin.

        Returns:
            Class instance.
        """
        repo = getattr(cls, dict(PLUGIN_SCOPE)[global_scope])

        for plugin_callable in plugin_callables:

            if hasattr(plugin_callable, 'func_name'):
                repo[plugin_callable.func_name] = plugin_callable
            else:  # pragma: no cover
                repo[plugin_callable.__name__] = plugin_callable

        return cls

    @classmethod
    def register_app(cls, application):
        """Register class view in bottle application.

        Args:
            application (instance): A bottle.Bottle() instance.

        Returns:
            Class instance.
        """

        if cls is BaseHandler:
            raise HandlerError("Cant register a `BaseHandler` class instance")

        routes = cls._get_http_members()

        router = getattr(application, "route")

        for func_name, func_callable in routes:
            # method_args = inspect.getargspec(func_callable)[0]
            # method_args.remove('self')

            method_args = inspect.signature(func_callable).parameters

            if hasattr(func_callable, 'http_method'):
                http_method = func_callable.http_method
                url_extra_part = func_callable.url_extra_part
            else:
                http_method = func_name
                url_extra_part = None

            applied_plugins = [pl for pl in cls.plugins
                               if hasattr(func_callable, pl)]

            for plugin in applied_plugins:  # pragma: no cover
                try:
                    func_callable = cls.plugins[plugin](func_callable)
                except TypeError as error:
                    raise HandlerPluginError(error.args)

            for global_plugin in cls.global_plugins:
                func_callable = cls.global_plugins[global_plugin](
                    func_callable
                )

            for entrypoint in cls._build_routes(method_args, url_extra_part):
                router(entrypoint, method=[http_method.upper()])(func_callable)

        if cls.cors_enabled:
            cls_desc = cls.__doc__ or ''
            options_data = {
                "handler": {"name": cls.__name__, "desc": cls_desc.strip()},
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

        return cls

    @classmethod
    def _build_routes(cls, method_args, url_extra_part=None):
        """Create bottle route for a handler http method."""

        prefix = '/{}'.format(url_extra_part) if url_extra_part else ''

        prefix += '/:' if method_args else ''

        endpoint = cls.base_endpoint + prefix

        if not method_args:
            return [endpoint]

        endpoints = []

        for args_list in cls._router_helper(method_args):
            endpoints.append((endpoint + '/:'.join(args_list)).replace("//", '/'))

        return endpoints

    @classmethod
    def _router_helper(cls, method_args):
        """Detect default Nullable method arguments and return
        multiple routes per callable.
        """

        fixed_params = [param for param in method_args
                        if method_args[param].default is not None]

        nullable_params = [param for param in method_args if param not in fixed_params]

        combinations = [fixed_params]

        combinations += [combinations[-1] + [param] for param in nullable_params]

        return combinations

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


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
