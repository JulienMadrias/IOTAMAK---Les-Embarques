import json
import config
from pyAmakCore.classes.amas import Amas
from sma_agent import SimpleAgent
from sma_environnement import SimpleEnvironment
import numpy as np
import pickle
import host
from state import State

import paho.mqtt.client as mqtt


class SimpleAmas(Amas):
    def __init__(self, execution_policy):
        super().__init__(SimpleEnvironment(), execution_policy)
        self.mqtt = mqtt.Client()
        self.connect_mqtt()

    def on_initial_agents_creation(self):
        ps = []
        for i in range(9):
            ps.append(SimpleAgent(i, self, self.get_environment().get_forks()[i],
                                  self.get_environment().get_forks()[i + 1]))

        ps.append(
            SimpleAgent(9, self, self.get_environment().get_forks()[9], self.get_environment().get_forks()[0]))

        for j in range(len(ps) - 1):
            ps[j + 1].add_neighbour(ps[j])
            ps[j].add_neighbour(ps[j + 1])

        ps[0].add_neighbour(ps[len(ps) - 1])
        ps[len(ps) - 1].add_neighbour(ps[0])
        self.add_agents(ps)

        # distribute agents
        # if we have 10 agents and 2 connected raspberry, we'll have 5 on each
        # let's assume we have 2 rasp
        # nb_raspberry = 2

        to_send = [list(elt)
                   for elt in np.array_split(ps, config.nb_raspberry)]

        client_sockets = host.accept_connection()

        # serialisation
        for i, agent_list in enumerate(to_send):
            with open(f'rasp_{i}', 'wb') as f:
                agents = []
                for agent in agent_list:
                    agents.append({
                        "id": agent._Agent__id,
                        "neighbours": [{
                            "id": neighbour._Agent__id,
                            # "left": neighbour._SimpleAgent__left._taken_by,
                            # "right": neighbour._SimpleAgent__right._taken_by
                        } for neighbour in agent._Agent__neighbours]
                    })

                    # for property, value in vars(agent).items():
                    #     print(property, ":", value)

                # print('*'*10, i)
                # print(agents)
                # print('*'*10)

                # serialize each agents list for eeach rasp
                with open(f'rasp_{i}', 'wb') as f:
                    pickle.dump(agents, f)

        # at some point we'll get the sockets

        for i, socket in enumerate(client_sockets):
            print(i)
            host.send_file(f'rasp_{i}', socket)

        # deserialisation
        # with open('rasp_0', 'rb') as f:
        #     r = pickle.load(f)
        #     for el in r:
        #         print(el._SimpleAgent__state)

    def connect_mqtt(self):
        self.mqtt.connect('localhost', 1883, 60)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.update_agents
        self.mqtt.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected... waiting for any published message")
        for i in range(9):
            client.subscribe("topic/sma/agent_"+str(i))

    def update_agents(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        payload = json.loads(payload)

        topic = topic.split('/')
        topic = topic[len(topic)-1:][0]

        if topic != 'cycle':
            # topic agent_*
            agent_id = int(topic.split('_')[1])

            for agent in self.get_agents():
                if agent.get_id() == agent_id:
                    agent.set_criticality(float(payload.get('criticality')))
                    agent._SimpleAgent__state = State(payload.get('state'))                    
