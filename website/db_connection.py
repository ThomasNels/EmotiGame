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

    # Execute table creation queries
    connection.execute_query(create_user_table)
    connection.execute_query(create_forms_table)

    # Close the connection
    connection.close()

if __name__ == "__main__":
    create_tables()
