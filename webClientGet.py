from socket import *

server_address = ('localhost', 8000)  # Specify the server's IP address and port
path = '/notFound'  # Specify the desired path

# Create a client socket
client_socket = socket(AF_INET, SOCK_STREAM)

# Connect to the server
client_socket.connect(server_address)

try:
    # Send an HTTP GET request with the specified path
    request = f"GET {path} HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client_socket.send(request.encode())

    # Receive and print the response
    response = client_socket.recv(4096).decode()
    print("HTTP response:\n", response)

finally:
    # Close the connection
    client_socket.close()
