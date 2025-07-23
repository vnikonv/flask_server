from flask import Blueprint, render_template, request, redirect, session, flash
from os import makedirs
from os.path import join, normpath, dirname
from app import STORAGE
from datetime import datetime

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads', methods=['GET']) # When the /uploads route is accessed, it will call the uploads function
@uploads_bp.route('/uploads?', methods=['GET'])
def uploads():
    mode = request.args.get('mode', '0')
    up_files = session.get('up_files', []) # Retrieves the list of uploaded files from the session, else defaults up_files to an empty array
    confirm = request.args.get('confirm', '0')
    return render_template('uploads.html', mode=mode, up_files=up_files, confirm=confirm) # The html file that lists uploaded files


@uploads_bp.route('/uploads/upload', methods=['POST']) # When the /upload route is accessed with a POST request, it will call the upload function
def upload():
    # If no files are selected, redirects to the uploads page
    if ('selected' not in request.files) or (request.files['selected'].filename == ''):
        flash('No files selected.', 'error')
        return redirect('/uploads')
    else:
        up_files = request.files.getlist('selected') # Variable for composing a user uploads history
        up_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for file in up_files: # Iterates through all files in the request and saves them to the server
            filepath = normpath(join(STORAGE, file.filename)) # Constructs the full path to the file in the storage directory, normalizing it to avoid directory traversal issues
            makedirs(dirname(filepath), exist_ok=True)  # Ensures that the directory exists before saving the file
            file.save(filepath) # Saves the file to the storage directory with a secure filename
        if session.get('up_files', None) is None:  # If the session does not have a list of uploaded files, initializes it
            session['up_files'] = [f'{file.filename} at {up_time}' for file in up_files]  # Saves the list of uploaded files in the session
        else: # If the session already has a list of uploaded files, appends the new files to it
            session['up_files'] += [f'{file.filename} at {up_time}' for file in up_files]
        flash(f'Files uploaded successfully at {up_time}.', 'success')
        return redirect('/uploads') # Redirects to the uploads page after saving files


@uploads_bp.route('/uploads/clear', methods=['POST']) # When the /uploads/clear route is accessed with a POST request (HTML does not natively support DELETE), it will call the clear_uploads function
def clear_uploads():
    """
    Clears the history of uploaded files from the session.
    """
    session['up_files'] = []  # Clears the list of uploaded files in the session
    flash('The uploads history is clear.', 'success')  # Flash message to indicate that the uploads history has been cleared
    return redirect('/uploads')  # Redirects to the uploads page after clearing the list

