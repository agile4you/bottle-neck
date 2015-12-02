# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.middleware` module.
"""


import pytest
import bottle_neck.middleware as middleware


@pytest.fixture(scope='module')
def mock_middleware():
    """pytest Fixture for 'bottle_neck.middleware.BaseMiddleware' subclass.
    """

    class MockMiddleware(middleware.BaseMiddleware):
        def __call__(self, e, h):
            e['PATH_INFO'] = e['PATH_INFO'].rstrip('/') + '#'
            return self.app(e, h)

    return MockMiddleware


def test_middleware_getattr(mock_middleware, mock_app):
    """Testing 'bottle_neck.middleware.BaseMiddleware' app wrapping method.
    """

    mock_app = mock_middleware(mock_app)

    assert mock_app.route


def test_middleware_getattr_multiple(mock_middleware, mock_app):
    """Testing 'bottle_neck.middleware.BaseMiddleware' app wrapping method
    for multiple wraps.
    """
    mock_app = mock_middleware(mock_middleware(mock_middleware(mock_app)))

    assert mock_app.route
