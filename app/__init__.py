from flask import Flask, session, render_template, url_for
from os.path import join, abspath, dirname
from os import makedirs

basedir = abspath(dirname(__file__)) # Path to the 'app/' directory
STORAGE = join(basedir, 'storage') # Directory to store the uploaded files

def create_app():
    app = Flask(__name__) # Initialized Flask

    makedirs(STORAGE, exist_ok=True) # Creates the storage directory if it does not exist

    @app.route('/', methods=['GET']) # When the root route is accessed, it will call the index function
    def index():
        return render_template('index.html') # The homepage is served

    from .routes.uploads import uploads_bp # Importing the uploads blueprint from routes module
    from .routes.downloads import downloads_bp # Importing the downloads blueprint from routes module

    app.register_blueprint(uploads_bp) # Registering the uploads blueprint with the Flask application
    app.register_blueprint(downloads_bp) # Registering the downloads blueprint with the Flask application

    return app
