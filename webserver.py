from socket import *
import sys 

server_socket = socket(AF_INET, SOCK_STREAM)  # Mengimport modul socket dan membuat objek server_socket dengan protokol IPv4 dan tipe soket TCP
server_address = ('', 8000)  # Menetapkan alamat IP dan nomor port untuk server
server_socket.bind(server_address)  # Mengikat socket server ke alamat dan port yang telah ditetapkan
server_socket.listen(1)  # Mendengarkan koneksi yang masuk dengan antrian sebanyak 1

while True:
    print('Ready to Serve')
    connection_socket, addr = server_socket.accept()  # Menerima koneksi baru dari client dan mengembalikan objek soket baru untuk berkomunikasi dengan client dan alamat client
    try:
        message = connection_socket.recv(1024).decode()  # Menerima pesan dari client sebesar 1024 byte dan mendekode pesan tersebut menjadi string
        filename = message.split()[1]  # Memecah pesan HTTP menjadi beberapa kata dan memperoleh nama file yang diminta oleh client
        f = open(filename[1:])  # Membuka file yang diminta oleh client
        outputdata = f.read()  # Membaca isi file yang diminta oleh client
        f.close()  # Menutup file yang telah dibuka
        connection_socket.send("HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n".encode())  # Mengirimkan status OK dan header respons kepada client
        for i in range(0, len(outputdata)):
            connection_socket.send(outputdata[i].encode())  # Mengirimkan isi file kepada client secara bertahap
        connection_socket.send("\r\n".encode())  # Mengirimkan karakter baru (CR LF) setelah isi file selesai dikirimkan
    except IOError:
        connection_socket.send("HTTP/1.1 404 Not Found\nContent-Type: text/html\r\n\r\n".encode())  # Mengirimkan status Not Found dan header respons kepada client jika file yang diminta tidak ditemukan
    connection_socket.close()  # Menutup objek socket yang digunakan untuk berkomunikasi dengan client
server_socket.close()  # Menutup objek socket server
sys.exit()  # Keluar dari program