# db_connection.py
import psycopg2

import os
from dotenv import load_dotenv

def load_database_information():
    load_dotenv()
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    return db_name, db_user, db_password

class DatabaseConnection:
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        db_name, db_user, db_password = load_database_information()
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

# Create tables if they don't exist
def create_tables():
    db_name, db_user, db_password = load_database_information()
    connection = DatabaseConnection('db_name', 'db_user', 'db_password')
    create_user_table = '''
    CREATE TABLE IF NOT EXISTS User_Information (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        name VARCHAR(100)
    );
    '''

    create_forms_table = '''
    CREATE TABLE IF NOT EXISTS FORMS (
        form_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES User_Information(user_id),
        forms TEXT
    );
    '''

    connection.execute_query(create_user_table)
    connection.execute_query(create_forms_table)
    connection.close()
