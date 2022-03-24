from flask import Blueprint, request, jsonify
from werkzeug.routing import BaseConverter
from functools import wraps
import datetime 

from jsonschema import Draft7Validator

class MissingAllOps(Exception):
    def __init__(self, missing):
        self.missing =  missing

class required(object):

    def __init__(self, schema):
        Draft7Validator.check_schema(schema)
        self.validator = Draft7Validator(schema=schema)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.content_type != 'application/json':
                return jsonify({
                    "This endpoint accepts only application/json"
                }),400

            body = request.get_json()

            if self.validator.is_valid(body):
                try:
                    return func(*args, body=body, **kwargs)
                except MissingAllOps as err:
                    missing = (f"`{field}`" for field in err.missing)
                    return jsonify(
                        {
                            "status":"error",
                            "msg": "Invalid request Body",
                            "errors": [f"One of {' or '.join(missing)} is required"]
                        }
                    ),400
            
            errors_message = [error.message for error in self.validator.iter_errors(body)]
            return jsonify({
                    "status":"error",
                    "msg": "Invalid request Body",
                    "errors": errors_message
            }), 400
        return wrapper



class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

def add_app_url_map_converter(self, func, name=None):
    """
    Register a custom URL map converters, available application wide.

    :param name: the optional name of the filter, otherwise the function name
                 will be used.
    """
    def register_converter(state):
        state.app.url_map.converters[name or func.__name__] = func

    self.record_once(register_converter)

# Custom Decorators

# Defining our custom decorator
def track_time_spent(name):
    # Link: https://stackoverflow.com/questions/16096211/custom-decorator-in-flask-not-working
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start = datetime.datetime.now()
            ret = f(*args, **kwargs)
            delta = datetime.datetime.now() - start
            print(name, "took", delta.total_seconds(), "seconds")
            return ret
        return wrapped
    return decorator

