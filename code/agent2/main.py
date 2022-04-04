import json
from sma_agent import SimpleAgent
import paho.mqtt.client as mqtt
import pickle
import socket
import tqdm
import os
import config

from sma_environnement import SimpleEnvironment

client = mqtt.Client()
client.connect(config.HOST, 1883, 60)

SEPARATOR = '<SEPARATOR>'
# receive 4096 bytes each time
BUFFER_SIZE = 4096

# create the client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    print(f'[+] Connecting to {config.HOST}:{config.PORT}')
    client_socket.connect((config.HOST, config.PORT))
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

agents = []
nb_agents = 0

# deserialisation
with open(filename, 'rb') as f:
    agents_prop_loaded = pickle.load(f)

    nb_agents = agents_prop_loaded[0].get('nb_agents')

    for agent_prop in agents_prop_loaded:
        agent = SimpleAgent(agent_prop.get('id'), agent_prop.get(
            'startX'), agent_prop.get('startY'))
        agents.append(agent)


def on_connect(client, userdata, flags, rc):
    print("Connected... waiting for any published message")
    client.subscribe("topic/sma/cycle")
    client.subscribe("topic/sma/env")
    for i in range(nb_agents):
        client.subscribe("topic/sma/agent_"+str(i))


def phase1(agent) -> None:
    """
    this is the first phase of a cycle
    """
    # if isinstance(agent, CommunicatingAgent):
    #     agent.read_mails()

    agent.on_perceive(agents)
    agent.set_criticality(agent.compute_criticality())
    agent.next_phase()


def phase2(agent) -> None:
    """
    this is the second phase of a cycle
    """
    agent.on_decide()
    agent.on_act()
    agent.set_criticality(agent.compute_criticality())
    agent.next_phase()


def new_cycle(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    payload = json.loads(payload)

    topic = topic.split('/')
    topic = topic[len(topic)-1:][0]

    if topic == 'cycle':
        # envoie de l'etat
        for agent in agents:
            #
            print('Coucou je suis l\'agent ', agent.get_id(),
                  '. Cycle ', payload)

            print('J\'envoie mon état actuel')
            # push my state
            client.publish("topic/sma/agent_"+str(agent.get_id()), json.dumps(
                {
                    'dx': agent.get_dx(),
                    'dy': agent.get_dy(),
                    'color': agent.color_to_int.get(agent.get_color())
                }
            ))

            agent.next_phase()

            # agent.on_cycle_begin()

            phase1(agent)

            agent.next_phase()

            phase2(agent)

            agent.on_act()

            # agent.on_cycle_end()
    elif topic == 'env':
        for agent in agents:
            # be aware of environment
            # print('Coucou je suis l\'agent ', agent.get_id(),
            #       '. J\'ai connaissance de l\'environnement : ', payload)

            # update agent environment
            env = SimpleEnvironment(xmin=payload.get('xmin'), ymin=payload.get('ymin'), xmax=payload.get(
                'xmax'), ymax=payload.get('ymax'), field_of_view=payload.get('field_of_view'), coef_deplacement=payload.get('coef_deplacement'))
            agent.set_environment(env)
    else:
        # topic agent_*
        agent_id = int(topic.split('_')[1])

        # for agent in agents:
        #     if agent.get_id() != agent_id:
        #         print(
        #             f'Agent {agent.get_id()} a reçu l\'état de son voisin Agent {agent_id}')

    # agent.on_cycle_end()


# specify callback functions
client.on_connect = on_connect
client.on_message = new_cycle

client.loop_forever()
