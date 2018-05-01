from my_app import api, db
from flask_restplus import Resource
from flask import jsonify
from database.models import *


@api.route('/test')
class TestApi(Resource):
    def get(self):
        test_array = {"test": "test_val"}
        #result = db.engine.execute('SELECT * from Etap').fetchone()
        result = Etap.query.first()
        etap = Etap(id=4, Nazwa_etapu='PogChamp')
        db.session.add(etap)
        db.session.commit()
        print(type(result))
        return jsonify(result.Nazwa_etapu)
