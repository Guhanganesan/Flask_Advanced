import os
from flask import Flask, g
from flask_cors import CORS 

def create_app():

    app = Flask(__name__)
    CORS(app)
    app.config["DEBUG"] = False 

    # set_environ_vars()

    from backend.routes.public import routes
    app.register_blueprint(routes.bp)

    # @app.before_request
    # def inject_session():
    #     g.get_session = session_getter

    return app

def set_environ_vars():
    # #Load Environment Variables
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")