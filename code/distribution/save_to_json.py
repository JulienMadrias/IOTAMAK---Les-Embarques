import json
import os


def save(data, filename):
    '''
    Permet d'enregistrer les logs dans un fichier au format JSON.
    '''

    if not os.path.isfile(filename):
        with open(filename, mode='w') as f:
            f.write(json.dumps([], indent=2))
    else:
        with open(filename) as fjson:
            logs = json.load(fjson)
            
        logs.append(data)

        with open(filename, mode='w') as f:
            f.write(json.dumps(logs, indent=2))
