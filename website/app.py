from flask import Flask, render_template
from flask.views import MethodView
from sessionManager import sessionManager
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')
    
app.add_url_rule('/login', view_func=sessionManager.as_view('login'), methods=['GET', 'POST'])

if __name__ == "__main__":
    # change debug to false to hide error from displaying on website, set to true for testing purposes
    app.run(debug=True)