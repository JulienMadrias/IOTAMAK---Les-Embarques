import socket
import tqdm
import os
import threading

HOST = '192.168.43.54'
PORT = 5001
FILENAME = 'code.zip'

SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 1024 * 4 #4KB


def accept_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print('listening on port:', server_socket.getsockname()[1])
        while True:
            client_socket, address = server_socket.accept()
            print(f'[+] {address} is connected.')
            send_file(FILENAME, client_socket)


def send_file(filename, client_socket):
    # get the file size
    filesize = os.path.getsize(filename)

    # send the filename and filesize
    client_socket.send(f'{filename}{SEPARATOR}{filesize}'.encode())

    # start sending the file
    progress = tqdm.tqdm(range(
        filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)
    with open(filename, 'rb') as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:                
                break
            client_socket.sendall(bytes_read)  

            progress.update(len(bytes_read))

    client_socket.close()

accept_connection()
