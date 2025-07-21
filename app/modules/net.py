"""
# This function retrieves the local IP address of the machine to be used by the Flask server.
"""
import socket

def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creates a UDP socket (connectionless, no handshake)
    try:
        s.connect(("8.8.8.8", 80)) # Determines which local IP address would be picked to route a packet to Google DNS, without actually sending any data
        ip = s.getsockname()[0] # Fetch local IP address
    finally:
        s.close() # Closes the socket
    return ip
