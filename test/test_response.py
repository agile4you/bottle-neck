# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.handlers` module.
"""


import pytest
import bottle_neck.response as response


def test_ws_response_init_pass():
    """Test `bottle_neck.response.WSResponse` init pass.
    """
    assert response.WSResponse(200, 1)


def test_ws_response_init_fail():
    """Test `bottle_neck.response.WSResponse` init pass.
    """
    with pytest.raises(response.WSResponseError):
        assert response.WSResponse(209, 1)


def test_ws_response_ok():
    """Test `bottle_neck.response.WSResponse.ok` method.
    """
    assert response.WSResponse.ok(data={"count": 1})


def test_ws_response_bad_request():
    """Test `bottle_neck.response.WSResponse.bad_request` method.
    """
    assert response.WSResponse.bad_request(errors=[1, 2])


def test_ws_response_created():
    """Test `bottle_neck.response.WSResponse.created` method.
    """
    assert response.WSResponse.created(data={})


def test_ws_response_not_modified():
    """Test `bottle_neck.response.WSResponse.not_modified` method.
    """
    assert response.WSResponse.not_modified()
