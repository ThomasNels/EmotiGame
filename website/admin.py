from flask import request, render_template, send_file, redirect, flash, url_for, session
from flask.views import View

class admin(View):
    """Class that manages the admin view for the website.
        TODO: List attributes for the class view.
    """
    def __init__(self):
        super().__init__()

    def upload_file(self):
        if request.method == "POST":
            file = request.files["file"]
            # TODO: call database class to upload file
            # TODO: add {file.database_file_field} to the return statement
            return f'Uploaded: '

    def dispatch_request(self):
        # TODO: update the code to reflect changes to to the database once made.
        # later it will check the session id for the admin field in the database.

        # check if user is admin and display page, else redirect to home page with message
        if session.get('user_id') == 1:
            return render_template('admin.html')
        else:
            flash('Sorry, you need to be an admin to access that page.')
            return redirect(url_for('index'))
    
