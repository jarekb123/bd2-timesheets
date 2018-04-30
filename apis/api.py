from my_app import api, db
from flask_restplus import Resource
from flask import jsonify
from database.models import Etap


@api.route('/test')
class TestApi(Resource):
    def get(self):
        test_array = {"test": "test_val"}
        #result = db.engine.execute('SELECT * from Etap').fetchone()
        result = Etap.query.first()
        print(type(result))
        return jsonify(result.Nazwa_etapu)
