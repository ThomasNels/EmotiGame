#A class to handle the login/logout functionality

#Libraries
from flask import request, redirect, url_for, session, render_template
from flask.views import View
from db_connection import DatabaseConnection
import os
from dotenv import load_dotenv

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
        self.userName = None
        self.password = None
        self.user_id = None
        self.action = action
        self.db_connection = DatabaseConnection(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))

    def __del__(self):
        self.db_connection.close()

    def auth(self):
        # Authenticates the user versus the database information
        query = """
        SELECT user_id, password FROM User_Information WHERE username = %s;
        """

        result = self.db_connection.fetch_one(query, (self.userName,))
        if result:
            stored_password = result[1]
            self.user_id = result[0]
            return stored_password == self.password  # TODO: Add hashing logic if needed (e.g., bcrypt)
        return False

    def create(self):
        # Creates a new user for the webstie
        if request.method == 'POST':
            # TODO: add name functionality
            new_username = request.form.get("new_username")
            new_email = request.form.get("new_email")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            if not new_username or not new_email or not new_password or not confirm_password:
                return render_template('create.html', create_user_message="All fields are required", create_user_success=False)

            if new_password != confirm_password:
                return render_template('create.html', create_user_message="Passwords do not match.", create_user_success=False)

            check_query = """
            SELECT user_id FROM User_Information WHERE username = %s OR email = %s;
            """
            existing_user = self.db_connection.fetch_one(check_query, (new_username, new_email))

            if existing_user:
                return render_template('create.html', create_user_message="Username or email already taken", create_user_success=False)

            # TODO: add hashing logic to password input

            # inserts information into the database
            insert_query = """
            INSERT INTO User_Information (username, email, password) VALUES (%s, %s, %s);
            """
            self.db_connection.execute_query(insert_query, (new_username, new_email, new_password))
            self.db_connection.close()

            return render_template('create.html', create_user_message="User created successfully", create_user_success=True)

        return render_template('create.html')

    def login(self):
        # Uses the auth function to ensure the user can login
        if self.auth():
            session['username'] = self.userName
            session['user_id'] = self.user_id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_message="Incorrect Username and/or password")

    #log out function
    def logout(self):
        #TODO: Have check to ensure user wants to logout
        session.pop('username', None)
        session.pop('user_id', None)
        return redirect(url_for('index'))

    #dispatch request funtion to get the username and password
    def dispatch_request(self):
        try:
            if self.action == 'login':
                if request.method == 'POST':
                    self.userName = request.form.get('username')
                    self.password = request.form.get('password')
                    return self.login()
                return render_template('login.html')

            if self.action == 'logout':
                return self.logout()

            if self.action == 'create':
                return self.create()

            # If no if condition is met, raise an exception
            raise ValueError("Invalid action specified")

        except Exception as e:
            # Handle the exception and return an error response
            return f"An error occurred: {e}", 400
