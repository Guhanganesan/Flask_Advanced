import os
import psycopg2


DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

def get_db_connection():

    # Connect to PostreSQL Database
    conn = psycopg2.connect(host='localhost',
                            database='test',
                            user=DB_USER,
                            password=DB_PASS)
    return conn