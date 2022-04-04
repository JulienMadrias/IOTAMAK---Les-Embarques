import socket
import tqdm
import os
import config
import sma_launch


SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 1024 * 4  # 4KB

server_socket = None


def accept_connection():
    client_sockets = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        global server_socket
        server_socket = s
        server_socket.bind((config.HOST, config.PORT))
        server_socket.listen(5)
        print('listening on port:', server_socket.getsockname()[1])
        connected_devices = 0
        while connected_devices < config.nb_raspberry:
            client_socket, address = server_socket.accept()
            print(f'[+] {address} is connected.')
            config.connected_rasp.append(address)

            client_sockets.append(client_socket)

            connected_devices += 1

    return client_sockets


def send_file(filename, client_socket):
    print
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


def close_socket():
    server_socket.close()
