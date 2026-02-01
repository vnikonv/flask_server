from flask import Flask, render_template, redirect, request, make_response
from os.path import join, abspath, dirname, exists
from os import symlink, makedirs
from app.modules.fman import env_read, env_write

basedir = abspath(dirname(__file__)) # Path to the 'app/' directory
STORAGE = join(basedir, 'storage') # Directory to store the uploaded files

def create_app(secret):
    app = Flask(__name__) # Initializes Flask
    app.secret_key = secret # Sets the secret key for the Flask app

    if env_read('.env', 'symlink') == '1': # If the symlink field is set to '1' in the .env file, create a symlink for the storage directory
        SYMLINK_SRC = env_read('.env', 'symlink_src') # Reads the symlink source path from the .env file
        if not exists(STORAGE):
            symlink(SYMLINK_SRC, STORAGE, target_is_directory=True) # Create a symlink from STORAGE to SYMLINK_SRC
    elif env_read('.env', 'symlink') is None:
        env_write('.env', 'symlink', '0') # Default to '0' if the symlink field does not exist
    if env_read('.env', 'symlink') == '0' and not exists(STORAGE):
        makedirs(STORAGE) # Creates the storage directory if it does not exist

    @app.route('/', methods=['GET']) # When the root route is accessed, it will call the index function
    def index():
        return render_template('index.html', theme = request.cookies.get('theme', 'dark')) # The homepage is served

    @app.route('/theme') # Route for changing the theme cookie
    def theme():
        response = make_response(redirect(request.referrer)) # Creates a response object to modify cookies
        theme = request.cookies.get('theme', 'dark') # Gets the theme from the theme cookie, defaults to 'dark'
        response.set_cookie('theme', 'light' if theme == 'dark' else 'dark') # Toggles the theme cookie between 'light' and 'dark'
        return response

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
