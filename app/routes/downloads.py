from flask import Blueprint, render_template, request, send_file, flash, redirect
from os import listdir, remove
from os.path import join, exists
from app import STORAGE

downloads_bp = Blueprint('downloads', __name__)

@downloads_bp.route('/downloads', methods=['GET', 'POST']) # When the /downloads route is accessed, it will call the list_files function that returns a list of links to files in storage folder
def list_files():
    files = listdir(STORAGE)
    confirm = False # Variable to determine if the user has confirmed to delete a file
    if request.method == 'POST' and request.form.get('confirm') == '1':
        confirm = True
    return render_template('downloads.html', files=files, confirm=confirm) # The html file that lists download links for files in the storage folder


@downloads_bp.route('/downloads/<file>') # When the /downloads/<filename> route is accessed, the server will send the selected file to the client
def send(file): # file is the name of the file to be sent, <> denotes a dynamic part of the route, meaning that <file> can be any filename
    return send_file(join(STORAGE, file), as_attachment=True)

@downloads_bp.route('/downloads/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """
    Deletes a file from the storage.
    """
    fpath = join(STORAGE, filename) # Constructs the full path to the file in the storage directory
    if exists(fpath):
        remove(fpath)
        flash(f'File {filename} deleted successfully.', 'success')
        return redirect('/downloads')  # Redirects to the downloads page after deleting the file