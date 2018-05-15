from my_app import api, app
from sqlalchemy.exc import DBAPIError, IntegrityError
from flask import jsonify


@app.errorhandler(IntegrityError)
@api.errorhandler(IntegrityError)
def db_errors_handler(error):
    return jsonify({
        'error': 'DB Error',
    }), 500
