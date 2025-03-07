import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables for the database, name the environment file .env
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
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query, params=None):
        """
        Execute a query and commit the transaction.
        """
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def fetch_one(self, query, params=None):
        """
        Execute a query and fetch a single result.
        """
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Exception as e:
            self.conn.rollback()
            raise e

    def execute_addition(self, participant_id, unparsed_file, mktracking_file, timestamp_data, recording_file, p_survey_file, g_survey_file, session_id, game):
        """
        Insert data into Sessions, Recordings, and Survey tables.
        """
        try:
            if session_id == 0:
                # Create a new session only if one does not exist already.
                self.cursor.execute(
                    sql.SQL("""
                        INSERT INTO Sessions (participant_id, unparsed_data, mktracking_data, timestamp_data)
                        VALUES (%s, %s, %s, %s)
                        RETURNING session_id;
                    """),
                    (participant_id, unparsed_file, mktracking_file, timestamp_data)
                )
                session_id = self.cursor.fetchone()['session_id']
                self.conn.commit()

            # Insert into Recordings table
            self.cursor.execute(
                sql.SQL("""
                    INSERT INTO Recordings (game, session_id, recording, recording_date)
                    VALUES (%s, %s, %s, NOW());
                """),
                (game, session_id, recording_file)
            )

            # Insert into Survey table
            if p_survey_file == 'None':
                self.cursor.execute(
                sql.SQL("""
                    INSERT INTO Survey (gameplay_survey, session_id, participant_id)
                    VALUES (%s, %s, %s);
                """),
                (g_survey_file, session_id, participant_id)
            )
            else:
                self.cursor.execute(
                    sql.SQL("""
                        INSERT INTO Survey (presence_survey, gameplay_survey, session_id, participant_id)
                        VALUES (%s, %s, %s, %s);
                    """),
                    (p_survey_file, g_survey_file, session_id, participant_id)
                )

            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def close(self):
        """
        Close the cursor and connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def create_tables():
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    if not db_name or not db_user or not db_password:
        raise ValueError("Database credentials are not properly set in the .env file")

    # Connect to the database
    connection = DatabaseConnection(db_name, db_user, db_password)

    create_activity_table = '''
    CREATE TABLE IF NOT EXISTS Activity (
        activity_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        activity_type VARCHAR
    );
    '''

    create_ethnicity_table = '''
    CREATE TABLE IF NOT EXISTS Ethnicity (
        ethnicity_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        ethnicity_type VARCHAR
    );
    '''

    # SQL statements to create tables
    create_participant_table = '''
    CREATE TABLE IF NOT EXISTS Participants (
        participant_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        participant_age INTEGER,
        ethnicity_id INTEGER REFERENCES Ethnicity(ethnicity_id),
        email VARCHAR,
        password VARCHAR,
        activity_id INTEGER REFERENCES Activity(activity_id),
        participant_height INTEGER,
        participant_weight INTEGER
    );
    '''

    create_sessions_table = '''
    CREATE TABLE IF NOT EXISTS Sessions (
        session_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        participant_id INTEGER REFERENCES Participants(participant_id),
        unparsed_data VARCHAR,
        mktracking_data VARCHAR,
        timestamp_data VARCHAR
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

    create_recordings_table = '''
    CREATE TABLE IF NOT EXISTS Recordings (
        recording_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        game VARCHAR,
        session_id INTEGER REFERENCES Sessions(session_id),
        recording VARCHAR,
        recording_date TIMESTAMP
    );
    '''

    create_survey_table = '''
    CREATE TABLE IF NOT EXISTS Survey (
        survey_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        participant_id INTEGER REFERENCES Participants(participant_id),
        presence_survey VARCHAR,
        gameplay_survey VARCHAR,
        session_id INTEGER REFERENCES Sessions(session_id)
    );
    '''

    connection.execute_query(create_activity_table)
    connection.execute_query(create_ethnicity_table)
    connection.execute_query(create_participant_table)
    connection.execute_query(create_sessions_table)
    connection.execute_query(create_recordings_table)
    connection.execute_query(create_survey_table)

    activity_levels = [
        "1 - Bedridden",
        "2 - Sedentary",
        "3 - Lightly Active",
        "4 - Moderately Active",
        "5 - Active",
        "6 - Very Active",
        "7 - Highly Active",
        "8 - Extremely Active",
        "9 - Semi-Professional Athlete",
        "10 - Professional Athlete"
    ]

    for activity in activity_levels:
        insert_activity_query = f'''
        INSERT INTO Activity (activity_type)
        VALUES ('{activity}');
        '''
        connection.execute_query(insert_activity_query)

    ethnicities = [
        "Caucasian",
        "African American",
        "Hispanic",
        "Asian",
        "Native American",
        "Pacific Islander",
        "Other"
    ]

    for ethnicity in ethnicities:
        insert_ethnicity_query = f'''
        INSERT INTO Ethnicity (ethnicity_type)
        VALUES ('{ethnicity}');
        '''
        connection.execute_query(insert_ethnicity_query)

    connection.close()

if __name__ == "__main__":
    create_tables()
