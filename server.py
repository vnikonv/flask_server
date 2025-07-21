"""
# Flask application to upload and download files by client devices of a local access network.
# No JavaScript is used.
# It is possible to upload and download multiple folders or files at once.
# To run server locally, install the requirements and run this file.
"""

"""
# This function retrieves the local IP address of the machine to be used by the Flask server.
"""
import socket

def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creates a UDP socket, no handshake
    try:
        s.connect(("8.8.8.8", 80)) # Forces to determine which local IP address would be used to send packets to the destination, Google DNS
        ip = s.getsockname()[0] # Fetch local IP address used for this connection
    finally:
        s.close() # Closes connection
    return ip


"""
# This function generates a secret key for the Flask application to sign secure user/client session cookies.
"""
import secrets

def keygen() -> str:
    return secrets.token_hex(64)  # Generates a random secret key of 64 bytes or 128 hex characters


"""
# This function allows to seek a file (.env) and read the value from a specified field.
# It returns the value of the field if it exists, or None if it does not.
"""
def env_read(path : str, field : str) -> str | None:
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.startswith(f'{field}='):
                    return line.strip().split('=', 1)[1] # Splits the line at the first '=' once and returns the second part (the value)
    else:
        return None


"""
# This function allows to write a value to a specified field in a file (.env).
"""
def env_write(path : str, field : str, value : str) -> None:
    with open(path, 'a') as f:
        f.write(f'{field}={value}\n')

"""
# The following code is related to the Flask application itself.
"""
from flask import Flask, render_template, url_for, redirect, request, session, flash, send_file
import os

app = Flask(__name__) # Initialized Flask

STORAGE = 'storage' # Directory to store uploaded files
os.makedirs(STORAGE, exist_ok=True)

@app.route('/', methods=['GET']) # When the root route is accessed, it will call the index function
def index():
    return render_template('index.html') # The html form for uploading files is served

@app.route('/uploads', methods=['GET']) # When the /uploads route is accessed, it will call the uploads function
def uploads():
    all_files = session.get('all_files', []) # Retrieves the list of uploaded files from the session, else defaults all_files to an empty array
    print(all_files) # Prints the list of uploaded files to the console for debugging purposes
    return render_template('uploads.html', all_files=all_files) # The html file that lists uploaded files

@app.route('/upload', methods=['POST']) # When the /upload route is accessed with a POST request, it will call the upload function
def upload():
    try:
        all_files = request.files.getlist('selected')
        session['all_files'] = [file.filename for file in all_files]  # Saves the list of uploaded files in the session
        for file in all_files: # Iterates through all files in the request and saves them to the server
            file.save(os.path.join(STORAGE, file.filename))
        return redirect('/uploads') # Redirects to the uploads page after saving files
    except:
        session['all_files'] = [] # If an error occurs, sets session cookie all_files to an empty list
        flash('No files uploaded', 'error')
        return redirect('/') # Redirects to the index page

@app.route('/downloads', methods=['GET']) # When the /download route is accessed, it will call the list_files function that returns a list of links to files in storage folder
def list_files():
    files = os.listdir(STORAGE)
    return render_template('downloads.html', files=files) # The html file that lists download links for files in the storage folder


@app.route('/downloads/<file>') # When the /download/<filename> route is accessed, the server will send the selected file to the client
def send(file): # file is the name of the file to be sent, <> denotes a dynamic part of the route, meaning that <file> can be any filename
    return send_file(os.path.join(STORAGE, file), as_attachment=True)


if __name__ == '__main__':
    if env_read('.env', 'SECRET') is None: # If the SECRET field does not exist in the .env file, generate a new secret key
        env_write('.env', 'SECRET', keygen()) # Generates a secret key and writes it to the .env file
    app.secret_key = env_read('.env', 'SECRET') # Reads the secret key from the .env file and sets it for the Flask app
    host_ip = get_ip() # Gets the host IP address
    app.run(host=host_ip, port=5001, debug=True) # Run the server on the host ip at the designated port
