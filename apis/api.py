from my_app import api, db
from flask_restplus import Resource
from flask import jsonify
from database.models import *


@api.route('/test')
class TestApi(Resource):
    def get(self):
        test_array = {"test": "test_val"}
        etap = Stage(name='PogChamp')
        db.session.add(etap)
        db.session.commit()
        return jsonify(test_array)
