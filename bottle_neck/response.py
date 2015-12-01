# -*- coding: utf-8 -*-
"""Unified Web Service Response Interface for JSON views.

Provides some base classes that implement a strict skeleton for
API response using all HTTP method available. The concept is to
have a unified response object for any web-service that is
framework-agnostic.


.. note::
    In beta version only JSON renderer is supported. Must implement
    additional renderer classes (SOAP, XML, YAML).
"""

from types import NoneType


__version__ = '0.0.1'
__author__ = 'Papavassileiou Vassilis'
__all__ = ['WSResponse']


HTTP_CODES = (
    (200, 'OK'),
    (201, 'Created'),
    (304, 'Not Modified'),
    (400, 'Bad Request'),
    (401, 'Unauthorized'),
    (403, 'Forbidden'),
    (404, 'Not Found'),
    (405, 'Method Not Allowed'),
    (501, 'Not Implemented'),
    (503, 'Service Unavailable')
)


class WSResponseException(Exception):
    """Base module exception
    """
    pass


class WSResponse(object):
    """Base web service response class.

    WSResponse class provides a unified API for HTTP responses.

    The Response body skeleton looks like this::

         {
            "status_code": 200,
            "status_txt": "OK",
            "response_data": {
                "id": 65234
                "username": "pav"
                "email": "pav@geotagaeroview.com"
            },
            "errors": []

        }

    Attributes:
        status_code (int): Response HTTP status code.
        data (dict): Response key/value data.
        errors (dict): Response key/value errors.

    Examples:
        >>> response = WSResponse(
        ...                 status_code=200,
        ...                 data='Hi'
        ...             )
        ...
        >>> print response.to_json
        {'status_code': 200, 'status_text': 'OK', 'data': 'Hi', 'errors': []}

    """
    __slots__ = ['status_code', 'data', 'errors']

    def __init__(self, status_code=200, data=None, errors=None):
        if status_code not in dict(HTTP_CODES) or\
                not isinstance(errors, (list, NoneType)):
            raise WSResponseException(
                'Invalid Response initialization.'
            )
        self.status_code = status_code
        self.data = data
        self.errors = errors

    def __repr__(self):  # pragma: no cover
        return "WebService Response: status={}, data={}".format(
            self.status_code, str(self.data)
        )

    def __eq__(self, other):  # pragma: no cover
        assert isinstance(other, WSResponse), 'Invalid Type for eq operator.'
        return self.status_code == other.status_code and \
            self.data == self.data

    __str__ = __repr__

    @classmethod
    def ok(cls, data):
        """Shortcut API for HTTP 200 `OK` response.

        Args:
            data (dict): Response key/value data.

        Returns
            WSResponse Instance.
        """
        return cls(
            status_code=200,
            data=data
        ).to_json

    @classmethod
    def created(cls, data=None):
        """Shortcut API for HTTP 201 `Created` response.

        Args:
            data (dict): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        return cls(201, data=data).to_json

    @classmethod
    def not_modified(cls, errors=None):
        """Shortcut API for HTTP 304 `Not Modified` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        return cls(304, None, errors).to_json

    @classmethod
    def bad_request(cls, errors=None):
        """Shortcut API for HTTP 400 `Bad request` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        return cls(400, errors=errors).to_json

    @classmethod
    def unauthorized(cls, errors=None):
        """Shortcut API for HTTP 401 `Unauthorized` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        return cls(401, errors=errors).to_json

    @classmethod
    def forbidden(cls, errors=None):
        """Shortcut API for HTTP 403 `Forbidden` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        return cls(403, errors=errors).to_json

    @classmethod
    def not_found(cls, errors=None):
        """Shortcut API for HTTP 404 `Not found` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        return cls(404, None, errors).to_json

    @classmethod
    def method_not_allowed(cls, errors=None):
        """Shortcut API for HTTP 405 `Method not allowed` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        return cls(405, None, errors).to_json

    @classmethod
    def not_implemented(cls, errors=None):
        """Shortcut API for HTTP 501 `Not Implemented` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        return cls(501, None, errors).to_json

    @classmethod
    def service_unavailable(cls, errors=None):
        """Shortcut API for HTTP 503 `Service Unavailable` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        return cls(503, None, errors).to_json

    @property
    def to_json(self):
        """Short cut for JSON response service data.

        Returns:
            Dict that implements JSON interface.
        """
        return dict({'status_code': self.status_code,
                     'status_text': dict(HTTP_CODES).get(self.status_code),
                     'data': self.data or {},
                     'errors': self.errors or []})


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
