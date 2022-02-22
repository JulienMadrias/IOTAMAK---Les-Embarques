import paho.mqtt.client as mqtt


#this is the publisher

client = mqtt.Client()
client.username_pw_set(username="mqtt",password="pass2mqtt")
client.connect("192.168.2.1",1883,60)

f = open ("result.txt", "rb")
data = f.read()

while (data):
	client.publish("topic/hello",data)
	data = f.read()
	f.close()
client.disconnect()
