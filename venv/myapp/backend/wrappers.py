from flask import Blueprint
from werkzeug.routing import BaseConverter
from functools import wraps
import datetime 

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
