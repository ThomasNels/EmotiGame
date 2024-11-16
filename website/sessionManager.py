#A class to handle the login/logout functionality

#Libraries
from flask import request, redirect, url_for, session, render_template
from flask.views import View
from db_connection import DatabaseConnection

#class definition
class sessionManager(View):
    #class attributes
    def __init__(self, action):
        self.userName = None
        self.password = None
        self.user_id = None
        self.action = action
        self.db_connection = DatabaseConnection('db_name', 'db_user', 'db_password')

    def __del__(self):
        self.db_connection.close()

    #authentication function
    def auth(self):
        #check log in infor with the database
        query = """
        SELECT user_id, password FROM User_Information WHERE username = %s;
        """

        result = self.db_connection.fetch_one(query, (self.userName,))
        if result:
            stored_password = result[1]
            self.user_id = result[0]
            return stored_password == self.password  # Add hashing logic if needed (e.g., bcrypt)
        return False

    #log in function
    def login(self):
        if self.auth():
            session['username'] = self.userName
            session['user_id'] = self.user_id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_message=error_message)

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

            # If no if condition is met, raise an exception
            raise ValueError("Invalid action specified")

        except Exception as e:
            # Handle the exception and return an error response
            return f"An error occurred: {e}", 400
        if self.action == 'login':
            if request.method == 'POST':
                self.userName = request.form.get('username')
                self.password = request.form.get('password')
                return self.login()
            return render_template('login.html')
        
        if self.action == 'logout':
            return self.logout()

