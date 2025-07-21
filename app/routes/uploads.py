from flask import Blueprint, render_template, request, redirect, session, flash
from os.path import join
from app import STORAGE

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads', methods=['GET', 'POST']) # When the /uploads route is accessed, it will call the uploads function
def uploads():
    confirm = False # Variable to determine if the user has confirmed to clear the uploads history
    if request.method == 'POST' and request.form.get('confirm') == '1':
        confirm = True
    up_files = session.get('up_files', []) # Retrieves the list of uploaded files from the session, else defaults up_files to an empty array
    return render_template('uploads.html', up_files=up_files, confirm=confirm) # The html file that lists uploaded files

@uploads_bp.route('/uploads/upload', methods=['POST']) # When the /upload route is accessed with a POST request, it will call the upload function
def upload():
    # If no files are selected, redirects to the uploads page
    if ('selected' not in request.files) or (request.files['selected'].filename == ''):
        flash('No files selected.', 'error')
        return redirect('/uploads')
    else:
        up_files = request.files.getlist('selected') # Variable for composing a user uploads history
        if session['up_files'] is None:  # If the session does not have a list of uploaded files, initializes it
            session['up_files'] = [file.filename for file in up_files]  # Saves the list of uploaded files in the session
        else: # If the session already has a list of uploaded files, appends the new files to it
            session['up_files'] += [file.filename for file in up_files]
        for file in up_files: # Iterates through all files in the request and saves them to the server
            file.save(join(STORAGE, file.filename))
        return redirect('/uploads') # Redirects to the uploads page after saving files

@uploads_bp.route('/uploads/clear', methods=['POST']) # When the /uploads/clear route is accessed with a POST request, it will call the clear_uploads function
def clear_uploads():
    """
    Clears the history of uploaded files from the session.
    """
    session['up_files'] = []  # Clears the list of uploaded files in the session
    flash('The uploads history is clear.', 'success')  # Flash message to indicate that the uploads history has been cleared
    return redirect('/uploads')  # Redirects to the uploads page after clearing the list