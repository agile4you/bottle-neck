# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015  Papavassiliou Vassilis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""`bottle-neck` project.

Provides useful utilities for creating web-services with bottle.py
micro-framework.
"""

from __future__ import absolute_import

__author__ = 'Papavassiliou Vassilis'
__date__ = '2016-1-26'
__version__ = '1.18'

__all__ = ['BaseHandler', 'BaseHandlerPlugin', 'route_method', 'plugin_method',
           'HandlerError', 'HandlerPluginError', 'HandlerHTTPMethodError',
           'WSResponse', 'Router', 'Route', 'RouteError', 'BasePlugin',
           'WrapErrorPlugin', 'BaseMiddleware', 'StripPathMiddleware',
           'cors_enable_hook', 'strip_path_hook', 'paginator', 'version']


from bottle_neck.cbv import (
    BaseHandler, BaseHandlerPlugin, route_method, plugin_method, HandlerError,
    HandlerPluginError, HandlerHTTPMethodError
)
from bottle_neck.response import (WSResponse, WSResponseError)
from bottle_neck.routing import (RouteError, Router, Route)
from bottle_neck.plugins import (BasePlugin, WrapErrorPlugin)
from bottle_neck.middleware import (BaseMiddleware, StripPathMiddleware)
from bottle_neck.webapi import (cors_enable_hook, strip_path_hook, paginator)


version = tuple(map(int, __version__.split('.')))
