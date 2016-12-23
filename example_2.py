from bottle_neck import BaseHandler
from bottle_neck import Router
from bottle import Bottle


class ResourceHandler(BaseHandler):
    """Test cbv functionality.
    """

    cors_enabled = True

    def get(self, uid=None):
        """Example GET method.
        """
        if uid:
            return {'resource': name, 'model': uid}
        return {"resource": name}

    def post(self):
        """Example POST method.
        """

        return {"resource": "created"}


router = Router()

api = Bottle()

router.register_handler(ResourceHandler, '/')

router.mount(api)

for route in api.routes:
    print(route)
