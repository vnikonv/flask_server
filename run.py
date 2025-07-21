"""
# Flask application to upload and download files by client devices of a local access network.
# No JavaScript is used.
# It is possible to upload and download multiple folders or files at once.
# To run the server locally, install the requirements and run this file.
"""
from app import create_app
from app.modules.fman import env_read, env_write # Functions to read and write environment variables from/to a .env file
from app.modules.crypt import keygen # Function to generate a secret key for the Flask application
from app.modules.net import get_ip # Function to get the local IP address of the machine

app = create_app() # Creates a Flask application instance using the factory function from app module/folder

if __name__ == '__main__':
    if env_read('.env', 'SECRET') is None: # If the SECRET field does not exist in the .env file, generate a new secret key
        env_write('.env', 'SECRET', keygen()) # Generates a secret key and writes it to the .env file
    app.secret_key = env_read('.env', 'SECRET') # Reads the secret key from the .env file and sets it for the Flask app
    host_ip = get_ip() # Gets the host IP address
    app.run(host=host_ip, port=5001, debug=True) # Run the server on the host ip at the designated port
