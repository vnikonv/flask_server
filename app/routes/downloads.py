from flask import Blueprint, render_template, request, send_file, flash, redirect
from os import listdir, remove, rmdir
from os.path import join, exists, isdir, relpath, normpath # normpath for OS-independent path normalization
from app import STORAGE
from app.modules.fman import rmrf  # Importing the rmrf function to handle recursive file deletion

downloads_bp = Blueprint('downloads', __name__)

@downloads_bp.route('/downloads/', defaults={'subpath': ''}, methods=['GET'])
@downloads_bp.route('/downloads/tree/', defaults={'subpath': ''}, methods=['GET'])
@downloads_bp.route('/downloads/tree/<path:subpath>', methods=['GET']) # Important to include <path:> converter to handle subdirectories, allows slashes
def list_files(subpath):
    """
    Lists files and directories in the given subpath of the storage folder.
    """
    current_path = join(STORAGE, subpath)
    if not exists(current_path) or not isdir(current_path):
        flash('Invalid directory path.', 'danger')
        return redirect('/downloads')
    items = listdir(current_path) # List all items in the current directory
    confirm = request.args.get('confirm', '0') # Get confirmation for deletion
    return render_template('downloads.html', items=items, subpath=subpath, confirm=confirm, STORAGE=STORAGE, join=join, isdir=isdir)


@downloads_bp.route('/downloads/download/<path:filepath>', methods=['GET'])
def send(filepath):
    """
    Sends a file or zips and sends a directory.
    """
    fpath = join(STORAGE, normpath(filepath))
    if not exists(fpath):
        flash('File not found.', 'danger')
        return redirect('/downloads')

    if isdir(fpath):  # If the path is a directory, zip it before sending
        return redirect('/downloads')
    else:      
        return send_file(fpath, as_attachment=True)


@downloads_bp.route('/downloads/delete/<path:filepath>', methods=['POST'])
def delete_file(filepath):
    """
    Deletes a file or directory from the storage.
    """
    fpath = join(STORAGE, filepath)
    rmrf(fpath) # Using the rmrf function to handle file or directory deletion
    flash(f'File {relpath(filepath)} deleted successfully.', 'success')
    return redirect(f'/downloads/{"/".join(filepath.split("/")[:-1])}')
