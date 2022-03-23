import json
from sma_agent import SimpleAgent
from fork import Fork
from state import State
import paho.mqtt.client as mqtt
import pickle


import socket
import tqdm
import os


HOST = '127.0.0.1'
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

agents = []

# deserialisation
with open(filename, 'rb') as f:
    agents_prop_loaded = pickle.load(f)

    for agent_prop in agents_prop_loaded:
        agent = SimpleAgent(agent_prop.get('id'), Fork(), Fork())
        agent.__neighbours = [SimpleAgent(
            neighbour.get('id'), Fork(), Fork()) for neighbour in agent_prop.get('neighbours')]
        agents.append(agent)


client = mqtt.Client()
client.connect('localhost', 1883, 60)


def on_connect(client, userdata, flags, rc):
    print("Connected... waiting for any published message")
    client.subscribe("topic/sma/cycle")
    for i in range(9):
        client.subscribe("topic/sma/agent_"+str(i))

# message recieving callback
# when a PUBLISH message is received from the server


def phase1(agent) -> None:
    """
    this is the first phase of a cycle
    """
    # if isinstance(agent, CommunicatingAgent):
    #     agent.read_mails()

    agent.on_perceive()
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
        for agent in agents:
            #
            print('Coucou je suis l\'agent ', agent.id(),
                  '. Cycle ', payload)

            print('J\'envoie mon état actuel')
            # push my state
            client.publish("topic/sma/agent_"+str(agent.id()), json.dumps(
                {
                    "id": agent.id(),
                    "state": agent.get_state(),
                    "criticality": agent.get_criticality()
                }
            ))

            agent.next_phase()

            # agent.on_cycle_begin()

            phase1(agent)

            agent.next_phase()

            phase2(agent)

            agent.on_act()

            # agent.on_cycle_end()

    else:
        # topic agent_*
        neighbour_id = int(topic.split('_')[1])

        if State(payload.get('state')) == State.EATING:
            print(f'L\'agent {neighbour_id} mange')
        elif State(payload.get('state')) == State.HUNGRY:
            print(f'L\'agent {neighbour_id} a trop faim')
        elif State(payload.get('state')) == State.THINK:
            print(f'L\'agent {neighbour_id} réfléchi, Ne pas déranger')

        # on a deux conditions :
        #   - soit l'agent qui vient de push son state est lui meme, on ne fait rien
        #   - soit c'est un agent, qui peut être ou non son voisin :
        #       * si c'est son voisin, on le met à jour
        #       sinon, on ne fait rien

        for agent in agents:            
            if agent.id() != neighbour_id:
                neighbours = agent.__neighbours
                for neighbour in neighbours:
                    if neighbour.id() == neighbour_id:
                        # on actualise
                        print(
                            f'Agent {agent.id()} a reçu l\'état de son voisin Agent {neighbour.id()}, mise à jour voisin')
                        neighbour.__criticality = payload.get('criticality')                        

    # agent.on_cycle_end()


# specify callback functions
client.on_connect = on_connect
client.on_message = new_cycle

client.loop_forever()
