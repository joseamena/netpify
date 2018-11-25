
import paho.mqtt.client as mqtt
import json

BROKER_IP = "68.183.18.142"
BROKER_PORT = 1883

def on_publish(client, userdata, result):
    print("data published: " + userdata)

def on_connect(client, userdata, flags, rc):
    print("Connected with code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect(BROKER_IP, BROKER_PORT)
# client.loop_forever()

def send_data(data):
    # data will be a dictionary, here we will just publish the data
    # using MQTT
    # for key, value in data.items():
    #     if isinstance(value, dict):
    #         send_data(value)
    #     else:
    #         pass
    client.publish("espol/fiec/power_factor", json.dumps(data))


