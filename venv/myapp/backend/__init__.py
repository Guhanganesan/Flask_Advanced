from flask import Flask, g
from flask_cors import CORS 

def create_app():

    app = Flask(__name__)
    CORS(app)
    app.config["DEBUG"] = False

    from backend.routes.public import routes
    app.register_blueprint(routes.bp)

    # @app.before_request
    # def inject_session():
    #     g.get_session = session_getter

    return app