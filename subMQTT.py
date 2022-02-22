import paho.mqtt.client as mqtt

#this is the subscriber


#connection success callback 
#when a CONNACK response is recieved from the server
def on_connect(client, userdata, flags, rc):
	print("Connected... waiting for any published message")
	client.subscribe("topic/hello")

#message recieving callback
#when a PUBLISH message is recieved from the server
def on_message(client, userdata, msg):
		data = msg.payload.decode() 
		print(data)
		client.disconnect()
		
#create a client instance
client = mqtt.Client()

#set username and password
client.username_pw_set(username="mqtt",password="pass2mqtt")

#connect to broker @IP PORT KEEPALIVE
client.connect("192.168.2.1",1883,60)

#specify callback functions
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
