"""Example Web API with bottle_neck library.
"""

from bottle_neck import BaseHandler, Router, WSResponse, StripPathMiddleware
from bottle import Bottle, run


# Fake Resource database.

resource_db = [
    {'id': '1', 'name': 'Foo'},
    {'id': '2', 'name': 'Bar'},
    {'id': '3', 'name': 'Fizz'},
    {'id': '4', 'name': 'Buzz'},
]


# Resource APIHandler

class ResourceHandler(BaseHandler):
    """API Handler for Data Resource.
    """
    base_endpoint = '/'
    cors_enabled = True

    def get(self, uid=None):
        """Example retrieve API method.
        """
        # Return resource collection

        if uid is None:
            return WSResponse.ok(data=resource_db)

        # Return resource based on UID.

        try:
            record = [r for r in resource_db if r.get('id') == uid].pop()

        except IndexError:
            return WSResponse.not_found(errors=['Resource with UID {} does not exist.'.format(uid)])

        return WSResponse.ok(data=record)

    def post(self):
        """Example POST method.
        """

        resource_data = self.request.json

        record = {'id': len(resource_db) + 1,
                  'name': resource_data.get('name')}

        resource_db.append(record)

        return WSResponse.ok(data=record)


router = Router()

api = StripPathMiddleware(Bottle())

router.register_handler(ResourceHandler, '/')

router.mount(api)

for i in api.routes:
    print(i)

if __name__ == '__main__':

    run(app=api, port=8776, reloader=True)
