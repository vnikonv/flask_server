"""
# Flask server to upload and download files by client devices of a local network.
# No JavaScript is used.
# It is possible to upload and download a folder or multiple files at once.
# To run server, install the requirements and run this file.
"""

from flask import Flask, request, send_file
import os

app = Flask(__name__) # Initialized Flask

STORAGE = 'storage' # Directory to store uploaded files
os.makedirs(STORAGE, exist_ok=True)

@app.route('/') # When the root route is accessed, it will call the index function
def index():
    return """
    <h1>Uploads Page</h1>
    <form method="POST" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    <br>
    <a href="/download">Downloads Page</a>
    """ # The html form for uploading files

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
    app.run(host='0.0.0.0', port=8000) # Run the server on all interfaces at port 8000