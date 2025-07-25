from flask import Flask, render_template, url_for
from os.path import join, abspath, dirname
from os import makedirs

basedir = abspath(dirname(__file__)) # Path to the 'app/' directory
STORAGE = join(basedir, 'storage') # Directory to store the uploaded files

def create_app(secret):
    app = Flask(__name__) # Initializes Flask
    app.secret_key = secret # Sets the secret key for the Flask app

    makedirs(STORAGE, exist_ok=True) # Creates the storage directory if it does not exist

    @app.route('/', methods=['GET']) # When the root route is accessed, it will call the index function
    def index():
        return render_template('index.html') # The homepage is served

    @app.after_request # Implements strict no-cache policy
    def add_no_cache_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache' # For HTTP/1.0
        response.headers['Expires'] = '0' # Ensures immediate expiration
        return response

    from .routes.uploads import uploads_bp # Importing the uploads blueprint from routes module
    from .routes.downloads import downloads_bp # Importing the downloads blueprint from routes module

    app.register_blueprint(uploads_bp) # Registering the uploads blueprint with the Flask application
    app.register_blueprint(downloads_bp) # Registering the downloads blueprint with the Flask application

    return app