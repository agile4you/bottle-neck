# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.routing` module.
"""


import pytest
import bottle_neck.routing as routing
import bottle_neck.cbv as handler


@pytest.fixture(scope='module')
def mock_router():
    """pytest fixture for `bottle_neck.routing.Router` class
    """

    return routing.Router()


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

    return MockHandler


def test_router_register_handler_fn_pass(mock_router):
    """Test `bottle_neck.routing.Router.register_handler` for function-based
    handler pass.
    """

    def fn():
        pass

    mock_router.register_handler(fn, entrypoint='/', methods=('GET', ))

    assert len(mock_router) == 1


def test_router_register_handler_fail(mock_router):
    """Test `bottle_neck.routing.Router.register_handler` error handling.
    """

    with pytest.raises(routing.RouteError):
        mock_router.register_handler('handler', entrypoint='/')


def test_router_register_handler_cbv_pass(mock_router, mock_handler):
    """Test `bottle_neck.routing.Router.register_handler` for class-based
    handler pass.
    """

    mock_router.register_handler(mock_handler, entrypoint='/api')

    assert len(mock_router) == 2


def test_router_mount_pass(mock_router, mock_app):
    """Test `bottle_neck.routing.Router.mount` method.
    """
    init_mounts = len(mock_app.routes)
    mock_router.mount(mock_app)

    assert len(mock_app.routes) > init_mounts
