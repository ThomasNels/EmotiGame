#A class to handle the login/logout functionality

#Libraries
from flask import request, redirect, url_for, session, render_template
from flask.views import View
from db_connection import DatabaseConnection
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

class sessionManager(View):
    """A basic session manager class to manage the session for a user logged in.
    Attributes:
        userName: string
        password: string
        user_id: int
        action: flask method
        db_connection: db_connection class for a database connection
    """
    def __init__(self, action):
        super().__init__()
        self.email = None
        self.password = None
        self.user_id = None
        self.action = action
        self.db_connection = DatabaseConnection(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))

    def __del__(self):
        self.db_connection.close()

    def auth(self):
        # Authenticates the user versus the database information
        query = """
        SELECT participant_id, password FROM Participants WHERE email = %s;
        """
        result = self.db_connection.fetch_one(query, (self.email,))
        if result:
            stored_password = result['password']
            self.user_id = result['participant_id']
            return bcrypt.checkpw(self.password.encode('utf-8'), stored_password.encode('utf-8'))
        return False

    def create(self):
        # Creates a new user for the webstie
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            age = request.form.get("age")
            activity_level = request.form.get("activity_level")
            ethnicity_id = request.form.get("ethnicity")
            other_ethnicity = request.form.get("other_ethnicity")
            weight = request.form.get("weight")
            height = request.form.get("height")

            # Validate required fields
            if not email or not password or not confirm_password or not age or not activity_level or not ethnicity_id or not weight or not height:
                return render_template('create.html', create_user_message="All fields are required", create_user_success=False)

            # Check if passwords match
            if password != confirm_password:
                return render_template('create.html', create_user_message="Passwords do not match.", create_user_success=False)

            # NOTE: probably not a long term solution. Will be replaced.
            if ethnicity_id == "7":
                if not other_ethnicity:
                    return render_template('create.html', create_user_message="Please specify your ethnicity.", create_user_success=False)

                # Insert the new ethnicity into the Ethnicity table
                insert_ethnicity_query = """
                INSERT INTO Ethnicity (ethnicity_type) VALUES (%s) RETURNING ethnicity_id;
                """
                result = self.db_connection.fetch_one(insert_ethnicity_query, (other_ethnicity,))
                if not result:
                    return render_template('create.html', create_user_message="Failed to create new ethnicity.", create_user_success=False)
                ethnicity_id = result['ethnicity_id']

            # Check if the email is already taken
            check_query = """
            SELECT participant_id FROM Participants WHERE email = %s;
            """
            existing_user = self.db_connection.fetch_one(check_query, (email,))
            if existing_user:
                return render_template('create.html', create_user_message="Email already taken", create_user_success=False)

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert the new user into the Participants table
            insert_query = """
            INSERT INTO Participants (email, password, participant_age, activity_id, ethnicity_id, participant_weight, participant_height)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            self.db_connection.execute_query(insert_query, (email, hashed_password.decode('utf-8'), age, activity_level, ethnicity_id, weight, height))
            self.db_connection.close()

            return render_template('create.html', create_user_message="User created successfully", create_user_success=True)

        return render_template('create.html')

    def login(self):
        # Uses the auth function to ensure the user can login
        if self.auth():
            session['email'] = self.email
            session['user_id'] = self.user_id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_message="Incorrect Email and/or password")

    def logout(self):
        session.pop('email', None)
        session.pop('user_id', None)
        return redirect(url_for('index'))

    def dispatch_request(self):
        try:
            if self.action == 'login':
                if request.method == 'POST':
                    self.email = request.form.get('email')
                    self.password = request.form.get('password')
                    return self.login()
                return render_template('login.html')

            if self.action == 'logout':
                return self.logout()

            if self.action == 'create':
                return self.create()

            raise ValueError("Invalid action specified")

        except Exception as e:
            return f"An error occurred: {e}", 400
