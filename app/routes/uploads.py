from flask import Blueprint, render_template, request, redirect, session, flash, make_response
from os import makedirs
from os.path import join, normpath, dirname, getsize
from app import STORAGE
from datetime import datetime
from json import loads, dumps

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/uploads', methods=['GET'])
# When the /uploads route is accessed, it will call the uploads function
@uploads_bp.route('/uploads?', methods=['GET'])
def uploads():
    mode = request.args.get('mode', '0')
    confirm = request.args.get('confirm', '0')
    up_files = eval(request.cookies.get('up_files', '[]')) # Gets the list of uploaded files from a cookie, else defaults up_files to an empty array
    up_sizes = eval(request.cookies.get('up_sizes', '[]'))
    up_times = eval(request.cookies.get('up_times', '[]'))
    return render_template('uploads.html', mode=mode, up_files=up_files, up_sizes=up_sizes, up_times=up_times, confirm=confirm, zip=zip,
    theme = request.cookies.get('theme', 'light'))
    # The html file that lists uploaded files


@uploads_bp.route('/uploads/upload', methods=['POST'])
# When the /upload route is accessed with a POST request, it will call the upload function
def upload():
    # If no files are selected, redirects to the uploads page
    if ('selected' not in request.files) or (request.files['selected'].filename == ''):
        flash('No files selected.', 'error')
        return redirect('/uploads')
    else:
        up_files = request.files.getlist('selected') # Variable that stores filenames in user uploads history
        response = make_response(redirect('/uploads')) # Allows to edit the response object and create cookies
        up_names = loads(request.cookies.get('up_files', '[]'))
        up_sizes = loads(request.cookies.get('up_sizes', '[]'))
        up_times = loads(request.cookies.get('up_times', '[]'))
        up_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        for file in up_files: # Iterates through all files in the request and saves them to the server
            filepath = normpath(join(STORAGE, file.filename))
            # Constructs the full path to the file in the storage directory, normalizing it to avoid directory traversal issues
            makedirs(dirname(filepath), exist_ok=True)  # Ensures that the directory exists before saving the file
            file.save(filepath) # Saves the file to the storage directory
            # Loads the list of uploaded files from the cookie, or initializes it as an empty list if the cookie does not exist
            up_names.append(file.filename) # Appends the filename to the list of uploaded files in the cookie
            size = getsize(filepath) # Gets the size of the uploaded file in bytes
            if size >= 1073741824: # Conditions to format the file size for display
                size = f'{"{:.2f}".format(size / 1073741824)} GB'
            elif size >= 1048576:
                size = f'{"{:.2f}".format(size / 1048576)} MB'
            elif size >= 1024:
                size = f'{"{:.2f}".format(size / 1024)} KB'
            else:
                size = f'{size} B'
            up_sizes.append(size) # Saves the file size in the cookie
            up_times.append(up_time)
        response.set_cookie('up_files', dumps(up_names)) # Sets the cookie with the updated list of uploaded files
        response.set_cookie('up_sizes', dumps(up_sizes)) # Sets the cookie with the updated list of file sizes
        response.set_cookie('up_times', dumps(up_times)) # Sets the cookie with the updated list of upload times
        # up_time has to be saved for every file, because of the way the uploads page is rendered,
        # so the cookie variable is saved as a list of the same length as the number of uploaded files
        flash(f'Files uploaded successfully at {up_time}.', 'success')
        return response # Redirects to the uploads page after saving files


@uploads_bp.route('/uploads/clear', methods=['POST'])
# When the /uploads/clear route is accessed with a POST request (HTML does not natively support DELETE), it will call the clear_uploads function
def clear_uploads():
    """
    Clears the history of uploaded files from the cookies.
    """
     # Clears the list of uploaded files in the cookie
    response = make_response(redirect('/uploads'))
    response.set_cookie('up_files', '[]')
    response.set_cookie('up_sizes', '[]')
    response.set_cookie('up_times', '[]')
    flash('The uploads history is clear.', 'success') # Flash message to indicate that the uploads history has been cleared
    return response # Redirects to the uploads page after clearing the list

