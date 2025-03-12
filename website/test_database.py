import unittest
import os
from unittest.mock import MagicMock, patch
from db_connection import DatabaseConnection

class TestExecuteAddition(unittest.TestCase):

    def setUp(self):
        # Mock the psycopg2.connect method to avoid real database connections
        # NOTE: Thank god for CS 333. We literally just learned about mocking.
        # Now I had to do a lot more research then what we learned, but at least I knew it existed.
        self.patcher = patch('psycopg2.connect', autospec=True)
        self.mock_connect = self.patcher.start()

        # Create a mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.instance = DatabaseConnection(db_name='test_db', user='test_user', password='test_password')

    def tearDown(self):
        self.patcher.stop()

    def test_new_session_creation(self):
        self.mock_cursor.fetchone.return_value = {'session_id': 123}

        # Call the function with session_id = 0
        self.instance.execute_addition(
            participant_id=1,
            unparsed_file="unparsed_data",
            mktracking_file="mktracking_data",
            recording_file="recording_data",
            p_survey_file="presence_survey",
            g_survey_file="gameplay_survey",
            session_id=0,
            game="game_name"
        )

        # Verify that a new session was created
        self.mock_cursor.execute.assert_any_call(
            unittest.mock.ANY,
            (1, "unparsed_data", "mktracking_data")
        )
        self.mock_cursor.fetchone.assert_called_once()
        self.mock_conn.commit.assert_called()

        # Verify that recordings and surveys were inserted with the new session_id
        self.mock_cursor.execute.assert_any_call(
            unittest.mock.ANY,
            ("game_name", 123, "recording_data")
        )
        self.mock_cursor.execute.assert_any_call(
            unittest.mock.ANY,
            ("presence_survey", "gameplay_survey", 123)
        )

    def test_existing_session(self):
        # Call the function with an existing session_id
        self.instance.execute_addition(
            participant_id=1,
            unparsed_file="unparsed_data",
            mktracking_file="mktracking_data",
            recording_file="recording_data",
            p_survey_file="presence_survey",
            g_survey_file="gameplay_survey",
            session_id=456,
            game="game_name"
        )

        # Verify that no new session was created
        # Check that the execute method was not called with the session creation query
        session_creation_call = (
            unittest.mock.ANY,  # SQL query
            (1, "unparsed_data", "mktracking_data")  # Parameters
        )
        assert session_creation_call not in self.mock_cursor.execute.call_args_list, \
            "Session creation query was called when it should not have been."

        # Verify that recordings and surveys were inserted with the provided session_id
        self.mock_cursor.execute.assert_any_call(
            unittest.mock.ANY,
            ("game_name", 456, "recording_data")
        )
        self.mock_cursor.execute.assert_any_call(
            unittest.mock.ANY,
            ("presence_survey", "gameplay_survey", 456)
        )

    def test_error_handling(self):
        # Simulate a database error
        self.mock_cursor.execute.side_effect = Exception("Database error")

        # Call the function and expect an exception
        with self.assertRaises(Exception):
            self.instance.execute_addition(
                participant_id=1,
                unparsed_file="unparsed_data",
                mktracking_file="mktracking_data",
                recording_file="recording_data",
                p_survey_file="presence_survey",
                g_survey_file="gameplay_survey",
                session_id=0,
                game="game_name"
            )

        # Verify that rollback was called
        self.mock_conn.rollback.assert_called_once()

    def test_resource_cleanup(self):
        # Call the function
        self.instance.execute_addition(
            participant_id=1,
            unparsed_file="unparsed_data",
            mktracking_file="mktracking_data",
            recording_file="recording_data",
            p_survey_file="presence_survey",
            g_survey_file="gameplay_survey",
            session_id=0,
            game="game_name"
        )

        # Verify that the cursor and connection were closed
        self.instance.close()
        self.mock_cursor.close.assert_called_once()
        self.mock_conn.close.assert_called_once()

def test_addition_with_new_session():
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    if not db_name or not db_user or not db_password:
        raise ValueError("Database credentials are not properly set in the .env file")

    with DatabaseConnection(db_name, db_user, db_password) as db:
        db.execute_addition(
            participant_id=1,
            unparsed_file="unparsed_data.txt",
            mktracking_file="mktracking_data.txt",
            recording_file="recording_data.txt",
            p_survey_file="presence_survey.txt",
            g_survey_file="gameplay_survey.txt",
            session_id=0,  # Indicates a new session
            game="Test Game"
        )

def test_addition_with_existing_session():
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    if not db_name or not db_user or not db_password:
        raise ValueError("Database credentials are not properly set in the .env file")

    with DatabaseConnection(db_name, db_user, db_password) as db:
        db.execute_addition(
            participant_id=1,
            unparsed_file="unparsed_data.txt",
            mktracking_file="mktracking_data.txt",
            recording_file="recording_data.txt",
            p_survey_file="presence_survey.txt",
            g_survey_file="gameplay_survey.txt",
            session_id=1,  # Use an existing session_id
            game="Test Game"
        )

if __name__ == "__main__":
    # NOTE: The two functions above should only be used if their is an existing user.
    test_addition_with_new_session()
    test_addition_with_existing_session()
    unittest.main()
