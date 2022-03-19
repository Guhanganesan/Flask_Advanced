import os
import psycopg2
from flask import Flask, render_template, url_for, request
app = Flask(__name__)

List = ["Raja","Anbu","Ganesan","Guhan"]

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
    conn = psycopg2.connect(host='localhost',
                            database='test',
                            user="postgres",
                            password="1234")
    return conn

@app.route('/get_db')
def get_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM employee;')
    emp = cur.fetchall()
    cur.close()
    conn.close()
    print(emp)
    return render_template('index.html', employee=emp)
	
if __name__=="__main__":
  app.run(debug = True)