# -*- coding: utf-8 -*-
"""Testing Class-Based web handlers dynamic routing.
"""

import bottle
from bottle_neck.handlers import BaseHandler, route_method, plugin_method
from bottle_neck.routing import Router


app = bottle.Bottle()


def print_plugin(handler):
    """Decorator that enforces request valid JSONEncoded body
    or raises 400 error.
    """
    def _decorator(*args, **kwargs):
        print 'Global plugin\n'
        return handler(*args, **kwargs)
    return _decorator


def json_body(handler):
    """Decorator that enforces request valid JSONEncoded body
    or raises 400 error.
    """
    def _decorator(*args, **kwargs):
        print 'Json plugin\n'
        return handler(*args, **kwargs)
    return _decorator


def log_plugin(handler):

    def _log_plugin(*args, **kwargs):
        print "Logging plugin\n"
        return handler(*args, **kwargs)
    return _log_plugin


class ModelHandler(BaseHandler):
    """Testing Model Handler.
    """
    base_endpoint = '/api'

    @plugin_method('json_body', 'log_plugin')
    def get(self, pk):
        return {"model": pk}

    def post(self):
        return {"created": 201}

    def put(self, pk):
        return {"updated": pk}

    @route_method('GET', extra_part=True)
    @plugin_method('log_plugin')
    def version(self):
        return {"version": '0.0.0'}


class UserHandler(BaseHandler):
    """Testing User Handler.
    """

    base_endpoint = '/user'

    def get(self, username):
        return {"user": username}


home = lambda: "Home page"
index = lambda: "Index page"
about = lambda: "About page"


#  ModelHandler.register_app(app)
#  UserHandler.register_app(app)


ModelHandler.add_plugin(
    scope='optional',
    plugin_callables=[json_body, log_plugin]
)

ModelHandler.add_plugin(
    scope='global',
    plugin_callables=[print_plugin]
)

print dir(ModelHandler.version)

router = Router()

router.add_handler(ModelHandler, entrypoint='/api2')
router.add_handler(UserHandler, entrypoint='/user2')
router.add_route('/home', ['GET'], home)
router.add_route('/index', ['POST'], index)
router.add_route('/about', ['GET'], about)


router.mount(app)

bottle.debug(True)
bottle.run(app=app, host='0.0.0.0', server="cherrypy", port=8183,
           reloader=True)