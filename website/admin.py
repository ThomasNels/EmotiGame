from flask import request, render_template, send_file, redirect, flash, url_for, session
from flask.views import View
from db_connection import DatabaseConnection
import os
from dotenv import load_dotenv

load_dotenv()

class admin(View):
    """Class that manages the admin view for the website.
        TODO: List attributes for the class view.
    """
    def __init__(self):
        super().__init__()
        self.db_connection = DatabaseConnection(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))

    def get_users(self):
        query = """
        SELECT participant_id FROM Participants;
        """
        self.db_connection.execute_query(query)
        all_users = [row['participant_id'] for row in self.db_connection.cursor.fetchall()]
        return all_users
    
    def get_sessions(self):
        query = """
        SELECT session_id FROM Sessions;
        """
        self.db_connection.execute_query(query)
        all_sessions = [row['session_id'] for row in self.db_connection.cursor.fetchall()]
        return all_sessions
    
    def upload_files(self, participant_id, session_id, files, gameplay_survey_file, presense_survey_file):
        base_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        data_dir = os.path.join(base_dir, 'session_data')
        participant_dir = os.path.join(data_dir, f'participant_{participant_id}_{session_id}')

        if not os.path.exists(data_dir):
           os.makedirs(data_dir)

        if not os.path.exists(participant_dir):
            os.makedirs(participant_dir)  
        
        for file_key, file in files.items():
            if file:
                file_path = os.path.join(participant_dir, file.filename)
                file.save(file_path)
                if file_key == 'emotibit_file':
                    unparsed_file = file_path
                elif file_key == 'tracking_file':
                    mktracking_file = file_path
                elif file_key == 'timestamp_file':
                    timestamp_file = file_path
                elif file_key == 'recording_file':
                    recording_file = file_path
        
        # TODO: add timestamp file to function, re-work function for exact files from admin (split apart), need way to get session_id if needed
        self.db_connection.execute_addition(participant_id=participant_id, unparsed_file=unparsed_file, mktracking_file=mktracking_file, timestamp_data=timestamp_file, 
                                            recording_file=recording_file, p_survey_file=presense_survey_file, g_survey_file=gameplay_survey_file,
                                            session_id=0, game='League of Legends')
   
    def dispatch_request(self):
        # NOTE: update to new database for admin privledge
        if session.get('user_id') == 1:
            if request.method == "POST":
                # dictionary used to get files
                user_id = request.form.get('user_id')
                session_id = request.form.get('session_id')
                print(type(session_id))
                print(session_id)
                files = {
                    'emotibit_file': request.files.get('emotibit_file'),
                    'tracking_file': request.files.get('tracking_file'),
                    'timestamp_file': request.files.get('timestamp_file'),
                    'recording_file': request.files.get('recording_file')
                }

                gameplay_survey_file = request.form.get('gameplay_survey')

                presense_survey_file = request.form.get('presense_survey')

                self.upload_files(user_id, session_id, files, gameplay_survey_file, presense_survey_file)

                flash('Successfully upload files')
                return redirect(url_for('index'))
            users = self.get_users()
            sessions = self.get_sessions()
            base_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            surveys_dir = os.path.join(base_dir, 'survey_files')

            if not os.path.exists(surveys_dir):
                os.makedirs(surveys_dir)
                
            surveys = [file for file in os.listdir(surveys_dir) if file.endswith('.csv')]
            return render_template('admin.html', users=users, sessions = sessions, surveys = surveys)
        else:
            flash('Sorry, you need to be an admin to access that page.')
            return redirect(url_for('index'))
