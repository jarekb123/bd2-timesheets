from my_app import api
from flask_restplus import Resource


@api.route('/test')
class TestApi(Resource):
    def get(self):
        test_array = {"test": "test_val"}
        return test_array