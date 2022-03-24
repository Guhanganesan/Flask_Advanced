from flask import Blueprint
from backend.wrappers import add_app_url_map_converter, RegexConverter, track_time_spent

# monkey-patch the Blueprint object to allow addition of URL map converters
Blueprint.add_app_url_map_converter = add_app_url_map_converter

# create the eyesopen Flask blueprint
bp = Blueprint('myblueprint', __name__, url_prefix="/v1")

bp.add_app_url_map_converter(RegexConverter, 'regex')

@bp.route("/test_public_routes", methods=["GET"])
def test_public_routes():
    return "Hello, I am new test routes...."


@bp.route('/foo')
@track_time_spent('foo')
def foo():
    print("foo")
    return "foo"
