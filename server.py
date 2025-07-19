"""
# Flask server to upload and download files by client devices of a local access network.
# No JavaScript is used.
# It is possible to upload and download a folder or multiple files at once.
# To run server, install the requirements and run this file.
"""

import socket

"""
This function retrieves the local IP address of the machine to be used by the Flask server.
"""
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creates a UDP socket, no handshake
    try:
        s.connect(("8.8.8.8", 80))  # Forces to determine which local IP address would be used to send packets to the destination, Google DNS
        ip = s.getsockname()[0]    # Fetch local IP address used for this connection
    finally:
        s.close() # Closes connection
    return ip


"""
The following code is related to the Flask server itself.
"""
from flask import Flask, render_template, url_for, request, send_file
import os

app = Flask(__name__) # Initialized Flask

STORAGE = 'storage' # Directory to store uploaded files
os.makedirs(STORAGE, exist_ok=True)

@app.route('/') # When the root route is accessed, it will call the index function, GET
def index():
    return render_template('index.html') # The html form for uploading files


@app.route('/upload', methods=['POST']) # When the /upload route is accessed with a POST request, it will call the upload function
def upload():
    f = request.files.get('file')
    if not f or f.filename == '':
        return "No file selected"
    f.save(os.path.join(STORAGE, f.filename))
    return "Uploaded successfully"


@app.route('/download') # When the /download route is accessed, it will call the list_files function that returns a list of files available for download
def list_files():
    files = os.listdir(STORAGE)
    links = ''.join(f'<a href="/download/{fn}">{fn}</a><br>' for fn in files)
    return f'<h1>Downloads</h1>{links}'


@app.route('/download/<filename>') # When the /download/<filename> route is accessed, the server will send the files to the client
def send(filename):
    return send_file(os.path.join(STORAGE, filename), as_attachment=True)


if __name__ == '__main__':
    host_ip = get_ip()  # Gets the host IP address
    app.run(host=host_ip, port=5001, debug=True) # Run the server on the host ip at the designated port
