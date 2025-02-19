import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    """
    This class manages database queries and connections for the website.
    Attributes: 
        conn: the connection to the database itself.
        cursor: the cursor to the connection.
    """
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
    create_participant_table = '''
    CREATE TABLE IF NOT EXISTS Participants (
        participant_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        participant_age INTEGER,
        ethnicity_id INTEGER REFERENCES Ethinicity(ethinicity_id),
        email VARCHAR,
        password VARCHAR,
        survey_id INTEGER REFERENCES Survey(survey_id),
        activity_id INTEGER REFERENCES Activity(activity_id),
        session_id INTEGER REFERENCES Sessions(session_id),
        participant_height INTEGER,
        participant_weight INTEGER
    );
    '''

    create_sessions_table = '''
    CREATE TABLE IF NOT EXISTS Sessions (
        session_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        unparsed_data BLOB,
        timestamp_data BLOB
    );
    '''

    create_recordings_table = '''
    CREATE TABLE IF NOT EXISTS Recordings (
        recording_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        game VARCHAR,
        session_id INTEGER REFERENCES Sessions(session_id),
        recording BLOB,
        recording_date DATETIME
    );
    '''

    create_ethnicity_table = '''
    CREATE TABLE IF NOT EXISTS Ethnicity (
        ethnicity_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        ethnicity_type VARCHAR
    );
    '''

    create_survey_table = '''
    CREATE TABLE IF NOT EXISTS Survey (
        survey_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        presence_survey BLOB,
        gameplay_survey BLOB,
        session_id INTEGER REFERNECES Sessions(session_id)
    );
    '''

    create_activity_table = '''
    CREATE TABLE IF NOT EXISTS Activity (
        activity_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        activity_type VARCHAR
    );
    '''

    # Execute table creation queries
    connection.execute_query(create_participant_table)
    connection.execute_query(create_sessions_table)
    connection.execute_query(create_recordings_table)
    connection.execute_query(create_ethnicity_table)
    connection.execute_query(create_survey_table)
    connection.execute_query(create_activity_table)

    # Close the connection
    connection.close()

if __name__ == "__main__":
    create_tables()
