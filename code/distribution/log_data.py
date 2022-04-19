import paho.mqtt.client as mqtt
import json

from save_to_json import save

HOST = 'localhost'
PORT = 1883
AGENTS = 50

client = mqtt.Client()
client.connect(HOST, PORT, 60)

cycle = None
new_data = {}
data_to_save = []


def on_connect(client, userdata, flags, rc):
    client.subscribe("topic/sma/cycle")
    for i in range(AGENTS):
        client.subscribe("topic/sma/agent_"+str(i))


def on_message(client, userdata, msg):
    global cycle
    global new_data

    topic = msg.topic
    topic = topic.split('/')
    topic = topic[len(topic)-1:][0]
    payload = msg.payload.decode()
    payload = json.loads(payload)

    if topic == 'cycle':
        cycle = payload

        # print(json.dumps(new_data))
        save(new_data, 'log.json')

    else:
        if cycle:
            try:
                new_data['cycle_' + str(cycle)].append(payload)
            except:
                new_data['cycle_' + str(cycle)] = []
                new_data['cycle_' + str(cycle)].append(payload)


client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
