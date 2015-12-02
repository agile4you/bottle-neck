# -*- coding: utf-8 -*-
"""Testing Class-Based web handlers dynamic routing.
"""

import bottle
from bottle_neck.handlers import BaseHandler, route_method, plugin_method
from bottle_neck.routing import Router
from bottle_neck.handlers import BasePlugin


app = bottle.Bottle()


class LogPlugin(BasePlugin):
    """Testing base plugin.
    """

    def __call__(self, *args, **kwargs):
        print "Log: (calling a plugin wrapped handler)"
        return self._wrapped(*args, **kwargs)


class KeyPlugin(BasePlugin):
    """Testing optional plugins
    """

    def __call__(self, *args, **kwargs):
        if int(kwargs['pk']) < 0:
            return {"error": "Primary Key must be positive!"}
        return self._wrapped(*args, **kwargs)


class ModelHandler(BaseHandler):
    """Testing Model Handler.
    """
    base_endpoint = '/api'
    cors_enabled = True

    @plugin_method('key_plugin')
    def get(self, pk):
        return {"model": pk}

    def post(self):
        return {"created": 201}

    def put(self, pk):
        return {"updated": pk}

    @route_method('GET', extra_part=True)
    def version(self):
        return {"version": '0.0.0'}


ModelHandler.add_plugin(
    global_scope=True,
    plugin_callables=[LogPlugin]
)


ModelHandler.add_plugin(
    global_scope=False,
    plugin_callables=[KeyPlugin]
)


def handler():
    return 'Hello world!'


router = Router()
router.register_handler(handler, entrypoint='/')
router.register_handler(ModelHandler, entrypoint='/api')

router.mount(app)

if __name__ == '__main__':

    bottle.debug(True)
    bottle.run(
        app=app,
        host='0.0.0.0',
        server="cherrypy",
        port=8183,
        reloader=True
    )