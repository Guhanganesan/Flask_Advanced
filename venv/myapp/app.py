import os
from backend import create_app, set_environ_vars


app = create_app()

# set_environ_vars()   


if __name__ == '__main__':
    app.run(debug = True)



# import os
# import psycopg2
# from flask import Flask, render_template, url_for, request, jsonify
# from dotenv import load_dotenv
# from flask_cors import cross_origin

# load_dotenv()


# app = Flask(__name__)

# List = ["Raja","Anbu","Ganesan","Guhan"]

# @app.route('/test')
# def test():
#     return "Hi Raja"

# @app.route('/')
# def index():
#     name = "Guhan Ganesan"
#     return render_template('index.html',user=name)

# @app.route('/check')
# def check():
#     print(request.url_rule)
#     return "Hello %s" %request.url_rule

# @app.route('/concepts')
# def concept():
#     name = "Guhan Ganesan"
#     return render_template('concepts.html', user=name, len=len(List), mylist=List)