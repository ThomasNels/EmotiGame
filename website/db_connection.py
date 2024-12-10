import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        # Initialize database connection
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
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
    # Load database credentials from environment
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    if not db_name or not db_user or not db_password:
        raise ValueError("Database credentials are not properly set in the .env file")

    # Connect to the database
    connection = DatabaseConnection(db_name, db_user, db_password)

    # SQL statements to create tables
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
    CREATE TABLE IF NOT EXISTS Forms (
        form_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES User_Information(user_id),
        forms TEXT
    );
    '''
    create_survey_table = '''
        CREATE TABLE IF NOT EXISTS Surveys (
            survey_id SERIAL PRIMARY KEY,
            q1 INTEGER,
            q2 INTEGER,
            q3 INTEGER,
            q4 INTEGER,
            q5 INTEGER,
            q6 INTEGER,
            q7 INTEGER,
            q8 INTEGER,
            q9 INTEGER,
            q10 INTEGER,
            q11 INTEGER,
            q12 INTEGER,
            q13 INTEGER,
            q14 INTEGER,
            q15 INTEGER,
            q16 INTEGER,
            q17 INTEGER,
            q18 INTEGER,
            q19 INTEGER,
            q20 INTEGER,
            q21 INTEGER,
            q22 INTEGER,
            q23 INTEGER,
            q24 INTEGER,
            q25 INTEGER,
            q26 INTEGER,
            q27 INTEGER,
            q28 INTEGER,
            q29 INTEGER,
            q30 INTEGER,
            q31 INTEGER,
            q32 INTEGER,
            q33 INTEGER,
            q34 INTEGER,
            q35 INTEGER
    );
    '''

    # Execute table creation queries
    connection.execute_query(create_user_table)
    connection.execute_query(create_forms_table)
    connection.execute_query(create_survey_table)

    # Close the connection
    connection.close()

if __name__ == "__main__":
    create_tables()
