from socket import *
import sys 
import os

server_socket = socket(AF_INET, SOCK_STREAM)  # Membuat objek server_socket dengan protokol IPv4 dan tipe soket TCP
server_address = ('', 8000)  # Menetapkan alamat IP dan nomor port untuk server
server_socket.bind(server_address)  # Mengikat socket server ke alamat dan port yang telah ditetapkan
server_socket.listen(1)  # Mendengarkan koneksi yang masuk dengan antrian sebanyak 1

while True:
    print('Ready to Serve')
    connection_socket, client_address = server_socket.accept()  # Menerima koneksi baru dari client dan mengembalikan objek soket baru untuk berkomunikasi dengan client dan alamat client
    try:
        message = connection_socket.recv(1024).decode()  # Menerima pesan dari client sebesar 1024 byte dan mendekode pesan tersebut menjadi string
        if not message:
            continue

        print('\nHTTP request:\n', message)

        # Parse HTTP request
        request = message.split('\r\n')[0].split()
        if len(request) < 3:
            continue
        method = request[0]
        uri = request[1]
        http_version = request[2]

        # Process HTTP GET request
        if method == 'GET':
            # Determine requested file
            filename = uri[1:]
            if filename == '':
                filename = 'index.html'
            filepath = os.path.join(os.getcwd(), filename)
            print(f'file path was {filepath}')

            # Check if file exists
            if not os.path.exists(filepath):
                # File not found
                raise IOError

            # Read file content
            with open(filepath, 'r') as f:
                file_content = f.read()

            # Create HTTP response message
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Content-Type: text/html\r\n\r\n'
            response += file_content

        # Process HTTP HEAD request
        elif method == 'HEAD':
            # Determine requested file
            filename = uri[1:]
            if filename == '':
                filename = 'index.html'
            filepath = os.path.join(os.getcwd(), filename)

            # Check if file exists
            if not os.path.exists(filepath):
                # File not found
                raise IOError

            # Create HTTP response message
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Content-Type: text/html\r\n\r\n'

        # Unsupported HTTP method
        else:
            response = 'HTTP/1.1 405 Method Not Allowed\r\n'

        # Send HTTP response
        connection_socket.send(response.encode())

    except IOError:
        # File not found
        response = 'HTTP/1.1 404 Not Found\r\n'
        response += 'Content-Type: text/html\r\n\r\n'
        response += '<h1>404 Not Found</h1>'
        connection_socket.send(response.encode())
        print(response)

    except Exception as e:
        print('Error:', e)

    finally:
        # Close connection
        connection_socket.close()

server_socket.close()
sys.exit()