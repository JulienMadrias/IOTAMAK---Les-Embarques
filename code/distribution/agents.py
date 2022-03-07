import socket
import tqdm
import os


HOST = '127.0.0.1'
PORT = 1234
SEPARATOR = '<SEPARATOR>'

# create the client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    print(f'[+] Connecting to {HOST}:{PORT}')
    client_socket.connect((HOST, PORT))
    print('[+] Connected.')

    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(1024).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)

    filesize = int(filesize)

    progress = tqdm.tqdm(range(
        filesize), f'Receiving {filename}', unit='B', unit_scale=True, unit_divisor=1024)
    with open(filename, 'wb') as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(1024)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
