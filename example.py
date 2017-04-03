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

    response_factory = WSResponse
    cors_enabled = True

    def get(self, uid=None):
        """Example retrieve API method.
        """
        # Return resource collection

        if uid is None:
            return self.response_factory.ok(data=resource_db)

        # Return resource based on UID.

        try:
            record = [r for r in resource_db if r.get('id') == uid].pop()

        except IndexError:
            return self.response_factory.not_found(errors=['Resource with UID {} does not exist.'.format(uid)])

        return self.response_factory.ok(data=record)

    def post(self):
        """Example POST method.
        """

        resource_data = self.request.json

        record = {'id': str(len(resource_db) + 1),
                  'name': resource_data.get('name')}

        resource_db.append(record)

        return self.response_factory.ok(data=record)

    def put(self, uid):
        """Example PUT method.
        """

        resource_data = self.request.json

        try:
            record = resource_db[uid]

        except KeyError:
            return self.response_factory.not_found(errors=['Resource with UID {} does not exist!'])

        record['name'] = resource_data.get('name')

        return self.response_factory.ok(data=record)

    def delete(self, uid):
        """Example DELETE method.
        """
        try:
            record = resource_db[uid].copy()

        except KeyError:
            return self.response_factory.not_found(errors=['Resource with UID {} does not exist!'])

        del resource_db[uid]

        return self.response_factory.ok(data=record)


router = Router()

api = StripPathMiddleware(Bottle())

router.register_handler(ResourceHandler, '/')

router.mount(api)

if __name__ == '__main__':

    run(app=api, port=8776, reloader=True)
