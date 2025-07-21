from flask import Blueprint, render_template, request, redirect, session, flash
from os.path import join
from app import STORAGE

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads', methods=['GET']) # When the /uploads route is accessed, it will call the uploads function
def uploads():
    all_files = session.get('all_files', []) # Retrieves the list of uploaded files from the session, else defaults all_files to an empty array
    return render_template('uploads.html', all_files=all_files) # The html file that lists uploaded files

@uploads_bp.route('/uploads/upload', methods=['POST']) # When the /upload route is accessed with a POST request, it will call the upload function
def upload():
    # If no files are selected, redirects to the uploads page
    if ('selected' not in request.files) or (request.files['selected'].filename == ''):
        flash('No files selected', 'error')
        return redirect('/uploads')
    else:
        all_files = request.files.getlist('selected')
        session['all_files'] = [file.filename for file in all_files]  # Saves the list of uploaded files in the session
        for file in all_files: # Iterates through all files in the request and saves them to the server
            file.save(join(STORAGE, file.filename))
        return redirect('/uploads') # Redirects to the uploads page after saving files
