from socket import * # Mengimpor modul socket

server_address = ('localhost', 8000)  # Tentukan alamat IP dan port server

client_socket = socket(AF_INET, SOCK_STREAM) # Buat socket klien

client_socket.connect(server_address) # Hubungkan ke server

Method = input("What Method Do You Need ? : ")  # Meminta pengguna memasukkan metode HTTP (HEAD atau GET)
path = input("input path : ")  # Meminta pengguna memasukkan jalur path

if Method == "HEAD" : #Jika Methode yang dipilih adalah HEAD
    try:
        # Kirim permintaan HTTP HEAD dengan path yang ditentukan
        request = f"HEAD {path} HTTP/1.1\r\nHost: localhost\r\n\r\n" #menginisiasi variable request dengan Method HEAD
        client_socket.send(request.encode()) #mengirim permintaan HTTP yang telah dibentuk dalam variabel

        # Terima dan cetak header respons
        response = b"" #mendefinisikan variabel response sebagai byte string (string dalam bentuk byte).
        while True:
            data = client_socket.recv(4096) # mengambil data yang diterima dari server melalui soket klien. recv(4096) dan di simpan dalam variabel data 
            response += data #menambahkan data yang diterima (data) ke variabel response.
            if b"\r\n\r\n" in response: #memeriksa apakah respons yang telah diterima dari server (response) telah mencakup pemisah header HTTP yang ditandai dengan \r\n\r\n.
                break # jika sudah diterima maka break
        
        headers, _ = response.split(b"\r\n\r\n", 1) #memisahkan respons yang diterima (response) menjadi dua bagian berdasarkan pemisah header HTTP (\r\n\r\n).
        headers = headers.decode() #mengubah bagian header yang merupakan byte string (headers) menjadi string biasa 
        print("HTTP response headers:\n", headers) #mencetak header respons yang telah didekode.

    finally:
        # Tutup koneksi
        client_socket.close()
elif Method == "GET" : 
    try:
        request = f"GET {path} HTTP/1.1\r\nHost: localhost\r\n\r\n" #menginisiasi variable request dengan Method GET
        client_socket.send(request.encode()) #mengirim permintaan HTTP yang telah dibentuk dalam variabel

        response = client_socket.recv(4096).decode() #Baris ini menerima data dari server menggunakan metode recv(4096) dan mengkonversinya menjadi string menggunakan metode decode()
        print("HTTP response:\n", response) #mencetak respons HTTP yang telah diterima dari server. 
    finally:
        # Tutup koneksi
        client_socket.close()
else :
    print("The Method what you need not supported yet")  # Metode yang diminta tidak didukung saat ini
