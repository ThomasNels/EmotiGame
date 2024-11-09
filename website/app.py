from flask import Flask, render_template
from flask.views import MethodView
from sessionManager import sessionManager
import secrets
from admin import admin

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')
    
#page routes
app.add_url_rule('/login', view_func=sessionManager.as_view('login', action='login'), methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=sessionManager.as_view('logout', action='logout'), methods=['GET'])
app.add_url_rule('/admin', view_func=admin.as_view('admin'), methods=['GET', 'POST'])

# NOTE: Temporary until figuring out best way for game analytics pages
@app.route('/chess')
def chess():
    return render_template('chess.html')

@app.route('/league_of_legends')
def league():
    return render_template('league.html')

@app.route('/valorant')
def valorant():
    return render_template('valorant.html')

@app.route('/rocket_league')
def rocket():
    return render_template('rocket.html')

if __name__ == "__main__":
    # change debug to false to hide error from displaying on website, set to true for testing purposes
    app.run(debug=True)