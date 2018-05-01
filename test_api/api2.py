from my_app import api
from flask_restplus import Resource


@api.route('/test2')
class Test2Api(Resource):
    def get(self):
        return {'test2': 'payload'}