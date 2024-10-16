from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # change debug to false to hide error from displaying on website, set to true for testing purposes
    app.run(debug=True)