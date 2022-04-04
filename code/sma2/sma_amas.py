import json
import config
from pyAmakCore.classes.amas import Amas
from sma_agent import SimpleAgent
import numpy as np
import pickle
import host

import paho.mqtt.client as mqtt


class SimpleAmas(Amas):
    def __init__(self, env, execution_policy):
        super().__init__(env, execution_policy)
        self.mqtt = mqtt.Client()
        self.connect_mqtt()

    def on_initialization(self) -> None:
        # self.set_do_log(True)
        self.add_ignore_attribute("_CommunicatingAgent__mailbox")

    def on_initial_agents_creation(self):
        all_agents = []
        for i in range(50):
            agent = SimpleAgent(
                i, self, self.get_environment().xmax/2, self.get_environment().ymax/2)
            all_agents.append(agent)
        self.add_agents(all_agents)

        # ************************************************************************ #
        to_send = [list(elt)
                   for elt in np.array_split(all_agents, config.nb_raspberry)]

        client_sockets = host.accept_connection()

        # serialisation
        for i, agent_list in enumerate(to_send):
            with open(f'rasp_{i}', 'wb') as f:
                agents = []
                for agent in agent_list:
                    agents.append({
                        'id': agent.get_id(),
                        'startX':  self.get_environment().xmax/2,
                        'startY': self.get_environment().ymax/2,
                        'nb_agents': len(all_agents)
                    })

                # serialize each agents list for eeach rasp
                with open(f'rasp_{i}', 'wb') as f:
                    pickle.dump(agents, f)

        # at some point we'll get the sockets
        for i, socket in enumerate(client_sockets):
            host.send_file(f'rasp_{i}', socket)

    def connect_mqtt(self):
        self.mqtt.connect(config.HOST, 1883, 60)
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.update_agents
        self.mqtt.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected... waiting for any published message")
        for i in range(len(self.get_agents())):
            client.subscribe("topic/sma/agent_"+str(i))

    def update_agents(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        payload = json.loads(payload)

        topic = topic.split('/')
        topic = topic[len(topic)-1:][0]

        agent_id = int(topic.split('_')[1])

        for agent in self.get_agents():
            if agent.get_id() == agent_id:
                agent._dx = payload.get('dx')
                agent._dy = payload.get('dy')
                agent._color = agent.int_to_color.get(payload.get('color'))
                print(f'*** Agent {agent_id} updated on server***')

    def update_environment(self):
        env = {
            'xmin': self.get_environment().get_xmin(),
            'ymin': self.get_environment().get_ymin(),
            'xmax': self.get_environment().get_xmax(),
            'ymax': self.get_environment().get_ymax(),
            'field_of_view': self.get_environment().get_field_of_view(),
            'coef_deplacement': self.get_environment().get_coef_deplacement()
        }

        self.mqtt.publish('topic/sma/env', json.dumps(env))
