import paho.mqtt.client as mqtt

HOST = 'localhost'
PORT = 1883
AGENTS = 50

client = mqtt.Client()
client.connect(HOST, PORT, 60)


def on_connect(client, userdata, flags, rc):
    for i in range(AGENTS):
        client.subscribe("topic/sma/agent_"+str(i))


def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print(data)


client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
