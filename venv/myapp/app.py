import os
import psycopg2
from flask import Flask, render_template, url_for, request, jsonify
from dotenv import load_dotenv
from flask_cors import cross_origin

load_dotenv()


app = Flask(__name__)

List = ["Raja","Anbu","Ganesan","Guhan"]

#Load Environment Variables
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASS")

@app.route('/test')
def test():
    return "Hi Raja"

@app.route('/')
def index():
    name = "Guhan Ganesan"
    return render_template('index.html',user=name)

@app.route('/check')
def check():
    print(request.url_rule)
    return "Hello %s" %request.url_rule

@app.route('/concepts')
def concept():
    name = "Guhan Ganesan"
    return render_template('concepts.html', user=name, len=len(List), mylist=List)


def get_db_connection():

    # Connect to PostreSQL Database
    conn = psycopg2.connect(host='localhost',
                            database='test',
                            user=user,
                            password=password)
    return conn

@app.route('/get_employee')
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

    except (Exception, psycopg2.Error) as error:
        return jsonify({
            "status":"error",
            "data": "Error while fetching employee details"
        })
        
@app.route('/publish_employee', methods=['POST'])
@cross_origin()
def publish_employee_details():
    try:
        #print("====================")
        body = request.get_json()
        #print(body)
        conn = get_db_connection()
        cur = conn.cursor()
        emp_data = list(body.get("employee_data"))
        for items in emp_data:
            #print(items.get('name'))
            postgres_insert_query = """ INSERT INTO  publish_employee(id, name, age, address, salary) VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (int(items.get('id')),items.get('name'), int(items.get('age')), items.get('address'), int(items.get('salary')))
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
        if conn:
            return jsonify({
                "status":"success",
                "msg": "successfully published employee details"
            })

    except (Exception, psycopg2.Error) as error:
        return jsonify({
            "status":"error",
            "data": "Error while submitting data. please check connection"
        })
        
        


if __name__=="__main__":
  app.run(debug = True)