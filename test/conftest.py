# -*- coding: utf-8 -*-
"""Unit Tests fixtures for `bottle_neck` package.
"""

__author__ = 'Papavassiliou Vassilis'


import pytest
from bottle_neck.handlers import BaseHandler


@pytest.fixture(scope='session')
def cbv_cls():
    """Returns a CBV handler.
    """

    class TestHandler(BaseHandler):
        cors_enabled = True
        plugins = []

    return TestHandler
