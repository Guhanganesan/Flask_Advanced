import jwt
import datetime
from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from backend.wrappers import add_app_url_map_converter, RegexConverter, track_time_spent, required, \
token_required

from database.connection import get_db_connection


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

@bp.route("/test_token", methods=["POST"])
@cross_origin()
@token_required
def test_token(token):

    return "Guhan Ganesan"



@bp.route('/get_employee')
@cross_origin()
def get_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM employee;')
        emp = cur.fetchall()
        cur.close()
        conn.close()
        print(emp)
        #return render_template('index.html', employee=emp)
        emp_data = []
    
        for emp in emp:
                temp = {"id":emp[0],"name":emp[1], "age":emp[2], "address":emp[3], "salary":emp[4]}
                emp_data.append(temp)

        return jsonify({
            "status":"success",
            "data": emp_data
        })

    except Exception as error:
        return jsonify({
            "status":"error",
            "data": "Error while fetching employee details"
        })


@bp.route('/publish_employee', methods=['POST'])
@cross_origin()
@token_required
def publish_employee_details(token):
    try:
        print("====================")
        body = request.get_json()
        print(body)
        conn = get_db_connection()
        cur = conn.cursor()
        emp_data = list(body.get("employee_data"))
        end_date = body.get("submit_date")
        for items in emp_data:
            print(items.get('name'))
            postgres_insert_query = """ INSERT INTO  publish_employee(id, name, age, address, salary, submit_date) VALUES (%s,%s,%s,%s,%s,%s)"""
            record_to_insert = (int(items.get('id')),items.get('name'), int(items.get('age')), items.get('address'), int(items.get('salary')),\
            end_date)
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
        if conn:
            return jsonify({
                "status":"success",
                "msg": "Successfully published employee details"
            })

    except Exception as error:
        return jsonify({
            "status":"error",
            "msg": "Error while submitting data. please check connection"
        })      


@bp.route('/submit_info', methods=['POST'])
@required({
    "type": "object",
    "properties": {
        "id":{"type":"integer"},
        "name":{"type":"string"},
        "info":{"type":"object"}
    },
    "required":["id","name","info"]
})

def submit_info(body):

    print(body)

    return "Test"
