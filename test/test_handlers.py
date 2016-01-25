# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.handlers` module.
"""

__author__ = 'Papavassiliou Vassilis'


import pytest
import bottle_neck.cbv as handler


@pytest.fixture(scope="module")
def mock_handler():
    """Pytest fixture for `bottle_neck.handlers.BaseHandler` subclass.
    """

    class MockHandler(handler.BaseHandler):
        """Web handler fixture class.
        """
        cors_enabled = True
        base_endpoint = '/mock'

        def get(self, mock_id):
            return mock_id

        @handler.route_method('GET', extra_part=True)
        @handler.plugin_method('mock_plugin')
        def version(self):
            return 0, 0, 1

    return MockHandler


@pytest.fixture(scope="module")
def mock_plugin():
    """Pytest fixture for `bottle_neck.handlers.BasePlugin` subclass.
    """

    class MockPlugin(handler.BaseHandlerPlugin):

        def apply(self, *args, **kwargs):
            try:
                kwargs['pk'] = int(kwargs['pk'])
            except ValueError:
                kwargs['pk'] = -1

            return self._wrapped(*args, **kwargs)

    return MockPlugin


def test_handler_route_method_function_pass():
    """Test `bottle_neck.handlers.route_method` function pass.
    """
    class TestCls(object):
        @handler.route_method('POST', extra_part=True)
        def fn(self):
            pass

    assert TestCls.fn.http_method == 'POST' \
        and TestCls.fn.url_extra_part is 'fn'


def test_handler_route_method_function_fail():
    """Test `bottle_neck.handlers.route_method` function fail.
    """

    with pytest.raises(handler.HandlerHTTPMethodError):
        class TestCls(object):
            @handler.route_method('PORT', extra_part=True)
            def fn(self):
                pass

        assert TestCls


def test_handler_plugin_method_function_pass():
    """Test `bottle_neck.handlers.route_method` function pass.
    """
    class TestCls(object):
        @handler.plugin_method('log', 'auth')
        def fn(self):
            pass

    assert TestCls.fn.log is TestCls.fn.auth is True


def test_handler_singleton(mock_handler):
    """Test `bottle_neck.handlers.BaseHandler` subclass for singleton pattern.
    """
    assert mock_handler() == mock_handler()


def test_handler_cls_attrs(mock_handler):
    """Test `bottle_neck.handlers.BaseHandler` subclass for init class attrs.
    """
    ch_attrs = ('plugins', 'global_plugins', 'base_endpoint', 'cors_enabled')

    assert set(ch_attrs).issubset(set(dir(mock_handler)))


def test_handler_cls_add_plugin_function_based(mock_handler):
    """Test `bottle_neck.handlers.BaseHandler` explicit adding a plugin.
    """
    def kwargs_plugin(handler):
        """Testing function-based plugin.
        """
        def _decorator(*args, **kwargs):  # pragma: no cover
            return handler(*args, **kwargs)

        return _decorator

    mock_handler.add_plugin(
        global_scope=False,
        plugin_callables=[kwargs_plugin]
    )

    assert 'kwargs_plugin' in mock_handler.plugins


def test_handler_add_plugin_class_based(mock_handler, mock_plugin):
    """Test `bottle_neck.handlers.BaseHandler.add_plugin` method.
    """
    mock_handler.add_plugin(
        global_scope=True,
        plugin_callables=[mock_plugin]
    )

    assert 'mock_plugin' in mock_handler.global_plugins
    assert mock_plugin in mock_handler.global_plugins.values()


def test_handler_register_class_fail(mock_app):
    """Test `bottle_neck.handlers.BaseHandler.register_app` method error
    handling.
    """

    with pytest.raises(handler.HandlerError):
        handler.BaseHandler.register_app(mock_app)


def test_handler_register_class_pass(mock_app, mock_handler):
    """Test `bottle_neck.handlers.BaseHandler.register_app` method.
    """

    mock_handler.register_app(mock_app)

    assert all(['/mock' in i.rule for i in mock_app.routes])
