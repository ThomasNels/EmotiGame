from flask import Flask, render_template
from flask.views import MethodView
from sessionManager import sessionManager
import secrets
from db_connection import create_tables
from admin import admin
from survey import Survey

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Creates the database tables from db_connection
create_tables()

@app.route('/')
def index():
    return render_template('index.html')

# Page routes
app.add_url_rule('/login', view_func=sessionManager.as_view('login', action='login'), methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=sessionManager.as_view('logout', action='logout'), methods=['GET'])
app.add_url_rule('/admin', view_func=admin.as_view('admin'), methods=['GET', 'POST'])
app.add_url_rule('/create', view_func=sessionManager.as_view('create', action='create'), methods=['GET', 'POST'])
app.add_url_rule('/survey', view_func=Survey.as_view('survey'), methods=['GET','POST'])

# NOTE: Temporary until figuring out best way for game analytics pages

@app.route('/league_of_legends')
def league():
    return render_template('league.html')

@app.route('/contributors')
def contributors():
    return render_template('contributors.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    # change debug to false to hide error from displaying on website, set to true for testing purposes
    app.run(debug=True)
