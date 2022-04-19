# IOTAMAK---Les-Embarques

## Dépendances

  * pip install paho-mqtt 
  * pip install tqdm
  
  
## Fichiers Config

  ### Sur les RPIs
  
  * Mettre l'adresse IP du serveur
  * Mettre le port

  ### Sur le Serveur
  
  * Mettre le nombre de RPI à connecter
  * Mettre l'adresse IP du serveur
  * Mettre le même port que sur les RPIs


 ## Fichiers à mettre sur les RPIs
 
 (Présents dans le dossier ./code/agent)
  * agent.py
  * config
  * main.py
  * tout les fichiers/classes utilisés par les agents (exemple: fork.py dans le SMA des philosophes)


### Modification à apporter dans le code

 ## Dans le fichier main du côté client
 
 Dans on_onnect: Mettre les agents auquel l'agent doit subscribe dès le départ
 Dans new_cycle: 
   -Si le topic est cycle: pour spécifier les paramètres que le client doit publier
   -Si le topic est env: pour des actions spécifiques en cas de mise à jour de l'environnement
   -Sinon: pour observer les voisins et réagir
