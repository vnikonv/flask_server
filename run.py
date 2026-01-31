from app import create_app
from app.modules.fman import env_read, env_write # Functions to read and write environment variables from/to a .env file
from app.modules.crypt import keygen # Function to generate a secret key for the Flask application
from app.modules.net import get_ip # Function to get the local IP address of the machine
from multiprocessing import cpu_count # Importing the cpu_count function to calculate the number of threads for Waitress based on CPU cores
from waitress import serve as run # Importing the Waitress server to serve the Flask application

if env_read('.env', 'SECRET') is None: # If the SECRET field does not exist in the .env file, generate a new secret key
    env_write('.env', 'SECRET', keygen()) # Generates a secret key and writes it to the .env file

app = create_app(secret=env_read('.env', 'SECRET')) # Creates a Flask application instance using the factory function from app module/folder

if __name__ == '__main__':
    host_ip = get_ip() # Gets the host IP address
    port = 8080 # Default port for the server
    threads = 2 * cpu_count() + 1
    # Calculates the number of threads for Waitress based on the number of CPU cores
    # Can be lowered to cpu_count() + 1 for lower resource usage, if there is no high concurrency
    print(f'Starting server at {host_ip}:{port} with {threads} threads.') # Prints the server start message with host IP and number of threads
    run(app, listen=f'{host_ip}:{port}', threads=threads, expose_tracebacks=True, max_request_body_size=4294967296) # Runs the Waitress server
