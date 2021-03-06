from sqlalchemy.orm.exc import UnmappedError
from functools import wraps


def handle_map_error(error_msg):
    def jsonify_error_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except UnmappedError:
                return {'error': error_msg}, 401
        return wrapper
    return jsonify_error_decorator
