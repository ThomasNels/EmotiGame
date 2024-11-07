from flask import Flask, render_template
from flask.views import MethodView
from sessionManager import sessionManager
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')
    
#page routes
app.add_url_rule('/login', view_func=sessionManager.as_view('login', action='login'), methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=sessionManager.as_view('logout', action='logout'), methods=['GET'])

#TODO: put the admin page in its own class to create a class based view
@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == "__main__":
    # change debug to false to hide error from displaying on website, set to true for testing purposes
    app.run(debug=True)