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
        SELECT user_id FROM User_Information;
        """
        self.db_connection.execute_query(query)
        all_users = [row[0] for row in self.db_connection.cursor.fetchall()]
        return all_users

    def dispatch_request(self):
        # NOTE: update to new database for admin privledge
        if session.get('user_id') == 1:
            if request.method == "POST":
                print("upload")
                print("Request Form Data:", request.form)
                # dictionary used to get files
                # TODO: Use dictionary to upload files 
                user_id = request.form.get('user_id')
                files = {
                    'emotibit_file': request.files.get('emotibit_file'),
                    'hr_file': request.files.get('hr_file'),
                    'tracking_file': request.files.get('tracking_file'),
                    'timestamp_file': request.files.get('timestamp_file'),
                    'dataframe_file': request.files.get('dataframe_file')
                }
                # TODO: call database class to upload file
                # TODO: add {file.database_file_field}?
                # TODO: Check if upload successful and change message based on success
                print(f'Uploaded: User_id = {user_id}, file: {files}')
                flash('Successfully upload files')
                return redirect(url_for('index'))
            users = self.get_users()
            return render_template('admin.html', users=users)
        else:
            flash('Sorry, you need to be an admin to access that page.')
            return redirect(url_for('index'))
