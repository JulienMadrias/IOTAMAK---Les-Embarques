import socket

ADRESSE = '192.168.2.2'
PORT = 1235

#create an INET, STREAMing socket
serveur = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

#connect to client
serveur.connect((ADRESSE , PORT))

print ('Connnexion vers ' + ADRESSE)

# File Transfer

fichier = open('hellothere.py', 'rb')
print ('Envoi du fichier')
message = fichier.read(50)

while(message):
	serveur.send(message)
	message = fichier.read(50)
fichier.close()
serveur.shutdown(socket.SHUT_WR)

# Command Transfer

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.connect((ADRESSE , PORT))

cmd ='python3 hellothere.py'
print(cmd)
serveur.send(cmd.encode())
serveur.shutdown(socket.SHUT_WR)


# closing
print( 'Arret du serveur.')
serveur.close()


