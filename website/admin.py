from flask import request, render_template, send_file
from flask.views import View

class admin(View):
    def __init__(self):
        super().__init__()

    def upload_file(self):
        if request.method == "POST":
            file = request.files["file"]
            # TODO: call database class to upload file
            # TODO: add {file.database_file_field} to the return statement
            return f'Uploaded: '

    def dispatch_request(self):
        return render_template('admin.html')
    