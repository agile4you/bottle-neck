# -*- coding: utf-8 -*-
"""Unit Tests fixtures for `bottle_neck` package.
"""

__author__ = 'Papavassiliou Vassilis'

# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.middleware` module.
"""


import pytest
import bottle


@pytest.fixture(scope="session")
def mock_app():
    """pytest fixture for `bottle.Bottle` instance.
    """
    return bottle.Bottle()