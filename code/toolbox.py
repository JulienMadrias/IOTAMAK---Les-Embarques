import paho.mqtt.client as mqtt
import numpy as np
import pickle
import json
import os


def connect_mqtt(connect_callback, message_callback, host='localhost', port: int = 1883, keepalive: int = 60):
    '''
    Connection à MQTT et spécification de callback.
    '''
    mqtt.connect(host, port, keepalive)
    mqtt.on_connect = connect_callback
    mqtt.on_message = message_callback
    mqtt.loop_start()


def split_agents(all_agents, nb_raspberry):
    '''
    Renvoie les agents séparés en plusieurs groupes en fonction du nombre de raspberry.

    Parameters
    ----------
    all_agents : list
        L'ensemble des agents créés dans l'AMAS.

    nb_raspberry : list
        Le nombre de raspberry.
    '''
    return [list(elt)
            for elt in np.array_split(all_agents, nb_raspberry)]


def serialize_agents(agents_to_send: list):
    '''
    Permet de sérialiser les `agents` créés depuis l'AMAS afin de les envoyer aux rasspberry qui 
    hébergent les agents.

    Parameters
    ----------
    agents_to_send : list
        Une liste de groupe d'agents par raspberry.
    '''
    for i, agent_list in enumerate(agents_to_send):
        with open(f'rasp_{i}', 'wb') as f:
            agents = []
            for agent in agent_list:
                agents.append({
                    'id': agent.get_id(),
                    # ajouter d'autres propriétés ici
                })

            # serialize each agents list for each rasp
            with open(f'rasp_{i}', 'wb') as f:
                pickle.dump(agents, f)


def new_cycle(client, userdata, msg, agents):
    '''
    Synchronise les `agents` déployés sur les raspberry.

    Parameters
    ----------
    agents : list
        Les agents sur la raspberry.
    '''
    topic = msg.topic
    payload = msg.payload.decode()
    payload = json.loads(payload)

    topic = topic.split('/')
    topic = topic[len(topic)-1:][0]

    if topic == 'cycle':
        # Gestion du cycle

        # envoie de l'etat
        for agent in agents:

            print('Coucou je suis l\'agent ', agent.get_id(),
                  '. Cycle ', payload)

            print('J\'envoie mon état actuel')
            # push my state
            client.publish("topic/sma/agent_"+str(agent.get_id()), json.dumps(
                {
                    'prop1': agent.get_prop1(),
                    'prop2': agent.get_prop2(),
                    'prop3': agent.get_prop3()
                }
            ))

            # ...

            agent.next_phase()

            # phase1(agent) # faire appel à la phase 1 sur l'agent

            agent.next_phase()

            # phase2(agent) # faire appel à la phase 2 sur l'agent

            agent.on_act()

            agent.on_cycle_end()

    elif topic == 'env':
        # Prendre connaissance de l'environnement

        for agent in agents:
            print('Coucou je suis l\'agent ', agent.get_id(),
                  '. J\'ai connaissance de l\'environnement : ', payload)

        # ...
    else:
        # Prendre connaissance des autres agents

        agent_id = int(topic.split('_')[1])

        for agent in agents:
            if agent.get_id() != agent_id:
                print(
                    f'Agent {agent.get_id()} a reçu l\'état de son voisin Agent {agent_id}')

        # ...


def save(data, filename):
    '''
    Enregistre les logs dans un fichier au format JSON.

    Parameters
    ----------
    data : any
        Nouvelle entrée à enregistrer.

    filename : any
        Nom du fichier de destination des enregistrements.
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
