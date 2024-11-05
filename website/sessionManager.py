#A class to handle the login/logout functionality

#Libraries
from flask import request, redirect, url_for, session, render_template
from flask.views import View

#class definition
class sessionManager(View):
    #class attributes
    def __init__(self, action):
        self.userName = None
        self.password = None
        self.action = action

    #authentication function
    def auth(self):
        #check log in infor with the database

        #temperary user
        users = {
            'test': '1234' #username:password
        }
        return users.get(self.userName) == self.password


    #log in function
    def login(self):
        if self.auth():
            session['username'] = self.userName
            return redirect(url_for('index'))
        else:
            error_message = "Username or password is inncorect. Please try again."
            return render_template('login.html', error_message=error_message)
        
    #log out function
    def logout(self):
        session.pop('username', None)
        return redirect(url_for('index'))
    
    #dispatch request funtion to get the username and password
    def dispatch_request(self):
        if self.action == 'login':
            if request.method == 'POST':
                self.userName = request.form.get('username')
                self.password = request.form.get('password')
                return self.login()
            return render_template('login.html')
        if self.action == 'logout':
            return self.logout()


