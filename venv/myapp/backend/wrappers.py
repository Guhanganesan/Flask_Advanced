from flask import Blueprint, request, jsonify
from werkzeug.routing import BaseConverter
from functools import wraps
import datetime
import os 
import jwt 


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


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        user = None
        secret_key = os.environ.get("SECRET_KEY")
        #print(secret_key)
        
        """
        Postman Headers:
        Content-Type: application/json
        x-access-key: DJHKJHSAJHJFSAHHLKSJKLDFSALKSD
        x-access-user: guhan
        """
        
        if 'x-access-user' in request.headers:
            print(request.headers['Authorization']) #For Bearer token use
            token = request.headers['Authorization']
            user = request.headers['x-access-user']
            #secret_key = os.environ.get("SECRET_KEY") if os.environ.get("SECRET_KEY") else request.headers['x-access-key']
            user_key = request.headers['x-access-key']
            encoded = jwt.encode({'user': user,'key':user_key, 'user_token':token}, user_key, algorithm='HS256')
            #print(encoded)
            #eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZ3VoYW4iLCJrZXkiOiJESkhLSkhTQUpISkZTQUhITEtTSktMREZTQUxLU0QifQ.2arwIepsSx7cgeyQZavjerXPEdqaNFEDwxdeKA_flQg
            # Verify in : https://jwt.io/
            decoded = jwt.decode(encoded,secret_key,algorithms="HS256")
            #print(decoded) # {'user': 'guhan', 'key': 'DJHKJHSAJHJFSAHHLKSJKLDFSALKSD'}
            if decoded["key"] == request.headers['x-access-key'] and decoded["user_token"] == request.headers['Authorization']:
                return f(user, *args, **kwargs)
            else:
                return jsonify({"status":"error validating your key"})

    return decorator


def encode_auth_token(self, user, secret_key):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
            'iat': datetime.datetime.utcnow(),
            'sub': user
        }
        return jwt.encode(
            payload,
            secret_key=secret_key,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token, secret_key):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, secret_key, algorithms="HS256")
        return payload['sub']
    except Exception as e:
        return e


