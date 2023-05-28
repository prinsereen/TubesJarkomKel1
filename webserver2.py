from socket import *  # Mengimpor modul socket
import sys  # Mengimpor modul sys
import os  # Mengimpor modul os

server_socket = socket(AF_INET, SOCK_STREAM)  # Membuat objek server_socket dengan protokol IPv4 dan tipe soket TCP
server_address = ('', 8000)  # Menetapkan alamat IP dan nomor port untuk server
server_socket.bind(server_address)  # Mengikat soket server ke alamat dan port yang telah ditetapkan
server_socket.listen(1)  # Mendengarkan koneksi yang masuk dengan antrian sebanyak 1

while True:
    print('Ready to Serve')
    connection_socket, client_address = server_socket.accept()  # Menerima koneksi baru dari client dan mengembalikan objek soket baru untuk berkomunikasi dengan client dan alamat client

    try:
        message = connection_socket.recv(1024).decode()  # Menerima pesan dari client sebesar 1024 byte dan mendekode pesan tersebut menjadi string
        if not message:
            continue  # Melanjutkan ke iterasi berikutnya jika pesan kosong

        print('\nHTTP request:\n', message)  # Menampilkan pesan permintaan HTTP dari klien

        # Parse HTTP request
        request = message.split('\r\n')[0].split()  # Memecah pesan HTTP menjadi bagian-bagian yang relevan
        if len(request) < 3:
            continue
        method = request[0]  # Mendapatkan metode HTTP dari pesan
        uri = request[1]  # Mendapatkan URI dari pesan
        http_version = request[2]  # Mendapatkan versi HTTP dari pesan

        # Process HTTP GET request
        if method == 'GET':
            # Determine requested file
            filename = uri[1:]  # Mengambil nama file dari URI
            if filename == '':
                filename = 'index.html'  # Jika URI kosong, gunakan file index.html
            filepath = os.path.join(os.getcwd(), filename)  # Menggabungkan direktori saat ini dengan nama file

            # Check if file exists
            if not os.path.exists(filepath):  # Memeriksa apakah file ada
                # File not found
                raise IOError

            # Read file content
            with open(filepath, 'r') as f:
                file_content = f.read()  # Membaca konten file

            # Create HTTP response message
            response = 'HTTP/1.1 200 OK\r\n'  # Membuat status baris tanggapan HTTP dengan kode status 200 OK
            response += 'Content-Type: text/html\r\n\r\n'  # Menambahkan header Content-Type ke tanggapan
            response += file_content  # Menambahkan konten file ke pesan tanggapan

        # Process HTTP HEAD request
        elif method == 'HEAD':
            # Determine requested file
            filename = uri[1:]  # Mengambil nama file dari URI
            if filename == '':
                filename = 'index.html'  # Jika URI kosong, gunakan file index.html
            filepath = os.path.join(os.getcwd(), filename)  # Menggabungkan direktori saat ini dengan nama file

            # Check if file exists
            if not os.path.exists(filepath):  # Memeriksa apakah file ada
                # File not found
                raise IOError

            # Create HTTP response message
            response = 'HTTP/1.1 200 OK\r\n'  # Membuat status baris tanggapan HTTP dengan kode status 200 OK
            response += 'Content-Type: text/html\r\n\r\n'  # Menambahkan header Content-Type ke tanggapan

            # Unsupported HTTP method
        else:
            response = 'HTTP/1.1 405 Method Not Allowed\r\n'  # Jika metode HTTP tidak didukung, membuat tanggapan HTTP dengan kode status 405 Method Not Allowed

        # Send HTTP response
        connection_socket.send(response.encode())  # Mengirim tanggapan HTTP ke klien dengan mengubahnya menjadi byte dan mengirimkannya melalui soket koneksi

    except IOError:
        # File not found
        response = 'HTTP/1.1 404 Not Found\r\n'  # Jika file tidak ditemukan, membuat tanggapan HTTP dengan kode status 404 Not Found
        response += 'Content-Type: text/html\r\n\r\n'  # Menambahkan header Content-Type ke tanggapan
        response += '<h1>404 Not Found</h1>'  # Menambahkan pesan HTML ke tanggapan
        connection_socket.send(response.encode())  # Mengirim tanggapan HTTP ke klien dengan mengubahnya menjadi byte dan mengirimkannya melalui soket koneksi

    except Exception as e:
        print('Error:', e)  # Menampilkan pesan kesalahan jika terjadi kesalahan selama penanganan permintaan

    finally:
        # Close connection
        connection_socket.close()  # Menutup soket koneksi setelah penanganan permintaan selesai

server_socket.close()  # Menutup soket server setelah loop while selesai
sys.exit()  # Menghentikan program secara keseluruhan

