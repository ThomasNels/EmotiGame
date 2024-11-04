#A class to handle the login/logout functionality

#Libraries
from flask import request, redirect, url_for, session, render_template
from flask.views import View

#class definition
class sessionManager(View):
    #class attributes
    def __init__(self):
        self.userName = None
        self.password = None

    #authentication function
    def auth(self):
        #check log in infor with the database

        #temperary user
        users = {
            'test': 'hi' #username:password
        }

        return users.get(self.userName) == self.password


    #log in function
    def login(self):
        if self.auth():
            session['username'] = self.userName
            return redirect(url_for('index'))
        else:
            return "<h1>Login Failed</h1>"
        
    #log out function
    def logout(self):
        session.pop('username', None)
        return redirect(url_for('login'))
    
    #dispatch request funtion to get the username and password
    def dispatch_request(self):
        if request.method == 'POST':
            self.userName = request.form.get('username')
            self.password = request.form.get('password')
            return self.login()
        return render_template('login.html')


