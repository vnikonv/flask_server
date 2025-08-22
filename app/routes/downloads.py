from flask import Blueprint, render_template, request, send_file, session, flash, redirect, make_response
from os import listdir, remove, rmdir, makedirs
from os.path import join, exists, isdir, relpath, normpath, dirname, getsize
# normpath for OS-independent path normalization
from app import STORAGE
from app.modules.fman import rmrf, arch
# Importing the rmrf function to handle recursive file deletion
from datetime import datetime

downloads_bp = Blueprint('downloads', __name__)

@downloads_bp.route('/downloads/', defaults={'subpath': ''}, methods=['GET'])
@downloads_bp.route('/downloads/?', methods=['GET'])
@downloads_bp.route('/downloads/tree/', defaults={'subpath': ''}, methods=['GET'])
@downloads_bp.route('/downloads/tree/<path:subpath>', methods=['GET'])
# Important to include <path:> converter to handle subdirectories, allows slashes
def list_files(subpath):
    """
    Lists files and directories in the given subpath of the storage folder.
    """
    current_path = join(STORAGE, subpath)
    session['subpath'] = subpath  # Store the subpath and current_path in the session for use in /downloads/upload route
    session['current_path'] = current_path
    if not exists(current_path) or not isdir(current_path):
        flash('Invalid directory path.', 'danger')
        return redirect('/downloads')
    items = listdir(current_path) # List all items in the current directory
    confirm = request.args.get('confirm', '0') # Get confirmation for deletion
    mode = request.args.get('mode', '0')
    return render_template('downloads.html', items=items, subpath=subpath, confirm=confirm,
    STORAGE=STORAGE, join=join, isdir=isdir, mode=mode, theme = request.cookies.get('theme', 'light'))


@downloads_bp.route('/downloads/download/<path:filepath>', methods=['GET'])
def send(filepath):
    """
    Sends a file or zips and sends a directory.
    """
    fpath = join(STORAGE, normpath(filepath))
    apath = join(STORAGE, 'archive')
    if not exists(fpath):
        flash('File not found.', 'danger')
        return redirect('/downloads')

    if isdir(fpath):  # If the path is a directory, zip it before sending
        return send_file(arch(apath, 'zip').compress(fpath), as_attachment=True)
    else:
        return send_file(fpath, as_attachment=True)


@downloads_bp.route('/downloads/delete/<path:filepath>', methods=['POST'])
def delete_file(filepath):
    """
    Deletes a file or directory from the storage.
    """
    fpath = join(STORAGE, filepath)
    rmrf(fpath) # Using the rmrf function to handle file or directory deletion
    flash(f'Item {relpath(filepath)} deleted successfully.', 'success')
    return redirect(f'/downloads/tree/{"/".join(filepath.split("/")[:-1])}')


@downloads_bp.route('/downloads/upload', methods=['POST'])
def upload_file():
    """
    Uploads files, folders and archives to the current directory.
    """
    if ('selected' not in request.files) or (request.files['selected'].filename == ''):
        flash('No files selected.', 'error')
        return redirect('/downloads/tree/')
    else:
        up_files = request.files.getlist('selected') # Variable that stores filenames in user uploads history
        session['up_files'] = session.get('up_files', [])
        session['up_sizes'] = session.get('up_sizes', [])
        session['up_times'] = session.get('up_times', [])
        # up_time has to be saved for every file, because of the way the uploads page is rendered,
        # so the session variable is saved as a list of the same length as the number of uploaded files
        up_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        for file in up_files: # Iterates through all files in the request and saves them to the server
            filepath = normpath(join(session.get('current_path', STORAGE), file.filename))
            # Constructs the full path to the file in the storage directory, normalizing it to avoid directory traversal issues
            makedirs(dirname(filepath), exist_ok=True)  # Ensures that the directory exists before saving the file
            file.save(filepath) # Saves the file to the storage directory
            session['up_files'].append(file.filename) # Saves the filename in the session
            size = getsize(filepath) # Gets the size of the uploaded file in bytes
            if size >= 1073741824: # Conditions to format the file size for display
                size = f'{"{:.2f}".format(size / 1073741824)} GB'
            elif size >= 1048576:
                size = f'{"{:.2f}".format(size / 1048576)} MB'
            elif size >= 1024:
                size = f'{"{:.2f}".format(size / 1024)} KB'
            else:
                size = f'{size} B'
            session['up_sizes'].append(size) # Saves the file size in the session
            session['up_times'].append(up_time)
        flash(f'Files uploaded successfully at {up_time}.', 'success')
        mark = '/downloads/tree/' + session.get('subpath', '')
        return redirect(mark)
        # Redirects to the directory that the file was uploaded from after saving files