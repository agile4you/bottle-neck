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


from bottle_neck import __version__
import bottle
import collections
import six

__author__ = 'Papavassiliou Vassilis'
__all__ = ['WSResponse', 'WSRealResponse', 'WSResponseError']


version = tuple(map(int, __version__.split('.')))

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


class WSResponseError(Exception):
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
        data (object): Response key/value data.
        errors (dict): Response key/value errors.

    Examples:
        >>> response = WSResponse(
        ...                 status_code=200,
        ...                 data='Hi'
        ...             )
        ...
        >>> response.to_json
        OrderedDict([('status_code', 200), ('status_text', 'OK'), ('data', 'Hi'), ('errors', [])])

    """
    __slots__ = ['status_code', 'data', 'errors']

    expose_status = False
    response = bottle.response

    def __init__(self, status_code=200, data=None, errors=None):
        if status_code not in dict(HTTP_CODES) or\
                not isinstance(errors, six.string_types + (list, tuple, type(None),)):
            raise WSResponseError('Invalid Response initialization.')
        self.status_code = status_code
        self.data = data

        if isinstance(errors, (six.string_types, )):
            errors = [errors]

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
    def from_status(cls, status_line, msg=None):
        """Returns a class method from bottle.HTTPError.status_line attribute.
        Useful for patching `bottle.HTTPError` for web services.

        Args:
            status_line (str):  bottle.HTTPError.status_line text.
            msg: The message data for response.

        Returns:
            Class method based on status_line arg.

        Examples:
            >>> status_line = '401 Unauthorized'
            >>> error_msg = 'Get out!'
            >>> resp = WSResponse.from_status(status_line, error_msg)
            >>> resp['errors']
            ['Get out!']
            >>> resp['status_text']
            'Unauthorized'
        """
        method = getattr(cls, status_line.lower()[4:].replace(' ', '_'))
        return method(msg)

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
        if cls.expose_status:
            cls.response.content_type = 'application/json'
            cls.response._status_line = '201 Created'

        return cls(201, data=data).to_json

    @classmethod
    def not_modified(cls, errors=None):
        """Shortcut API for HTTP 304 `Not Modified` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        if cls.expose_status:
            cls.response.content_type = 'application/json'
            cls.response._status_line = '304 Not Modified'

        return cls(304, None, errors).to_json

    @classmethod
    def bad_request(cls, errors=None):
        """Shortcut API for HTTP 400 `Bad Request` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        if cls.expose_status:
            cls.response.content_type = 'application/json'
            cls.response._status_line = '400 Bad Request'

        return cls(400, errors=errors).to_json

    @classmethod
    def unauthorized(cls, errors=None):
        """Shortcut API for HTTP 401 `Unauthorized` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        if cls.expose_status:
            cls.response.content_type = 'application/json'
            cls.response._status_line = '401 Unauthorized'

        return cls(401, errors=errors).to_json

    @classmethod
    def forbidden(cls, errors=None):
        """Shortcut API for HTTP 403 `Forbidden` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        if cls.expose_status:
            cls.response.content_type = 'application/json'
            cls.response._status_line = '403 Forbidden'

        return cls(403, errors=errors).to_json

    @classmethod
    def not_found(cls, errors=None):
        """Shortcut API for HTTP 404 `Not found` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        if cls.expose_status:
            cls.response.content_type = 'application/json'
            cls.response._status_line = '404 Not Found'

        return cls(404, None, errors).to_json

    @classmethod
    def method_not_allowed(cls, errors=None):
        """Shortcut API for HTTP 405 `Method not allowed` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        if cls.expose_status:
            cls.response.content_type = 'application/json'
            cls.response._status_line = '405 Method Not Allowed'

        return cls(405, None, errors).to_json

    @classmethod
    def not_implemented(cls, errors=None):
        """Shortcut API for HTTP 501 `Not Implemented` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        if cls.expose_status:
            cls.response.content_type = 'application/json'
            cls.response._status_line = '501 Not Implemented'

        return cls(501, None, errors).to_json

    @classmethod
    def service_unavailable(cls, errors=None):
        """Shortcut API for HTTP 503 `Service Unavailable` response.

        Args:
            errors (list): Response key/value data.

        Returns:
            WSResponse Instance.
        """
        if cls.expose_status:
            cls.response.content_type = 'application/json'
            cls.response._status_line = '503 Service Unavailable'

        return cls(503, None, errors).to_json

    @property
    def to_json(self):
        """Short cut for JSON response service data.

        Returns:
            Dict that implements JSON interface.
        """

        web_resp = collections.OrderedDict()

        web_resp['status_code'] = self.status_code
        web_resp['status_text'] = dict(HTTP_CODES).get(self.status_code)
        web_resp['data'] = self.data if self is not None else {}
        web_resp['errors'] = self.errors or []

        return web_resp


class WSRealResponse(WSResponse):
    """A WSResponse subclass that exposes state to HTTP(S semantics.
    """
    expose_status = True


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
