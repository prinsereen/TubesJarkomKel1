from socket import *

server_address = ('localhost', 8000)  # Specify the server's IP address and port
path = '/anjay'  # Specify the desired path

# Create a client socket
client_socket = socket(AF_INET, SOCK_STREAM)

# Connect to the server
client_socket.connect(server_address)

try:
    # Send an HTTP HEAD request with the specified path
    request = f"HEAD {path} HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client_socket.send(request.encode())

    # Receive and print the response headers
    response = b""
    while True:
        data = client_socket.recv(4096)
        response += data
        if b"\r\n\r\n" in response:
            break
    
    headers, _ = response.split(b"\r\n\r\n", 1)
    headers = headers.decode()
    print("HTTP response headers:\n", headers)

finally:
    # Close the connection
    client_socket.close()
