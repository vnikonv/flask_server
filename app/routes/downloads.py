from flask import Blueprint, render_template, send_file
from os import listdir
from os.path import join
from app import STORAGE

downloads_bp = Blueprint('downloads', __name__)

@downloads_bp.route('/downloads', methods=['GET']) # When the /downloads route is accessed, it will call the list_files function that returns a list of links to files in storage folder
def list_files():
    files = listdir(STORAGE)
    return render_template('downloads.html', files=files) # The html file that lists download links for files in the storage folder


@downloads_bp.route('/downloads/<file>') # When the /downloads/<filename> route is accessed, the server will send the selected file to the client
def send(file): # file is the name of the file to be sent, <> denotes a dynamic part of the route, meaning that <file> can be any filename
    return send_file(join(STORAGE, file), as_attachment=True)
