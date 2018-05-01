from my_app import api
from flask_restplus import Resource


@api.route('/api')
class Api(Resource):
    def get(self):
        return "get /api"
