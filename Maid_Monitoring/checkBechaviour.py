import dill as pickle
import nltk
from nltk.lm import MLE
import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.hivemq.com'
port = 1883
topic = "sensors/control/maid"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = ''
password = ''

# Actual Working Beyond This Point
with open('Maid_Monitoring/maid_monitoring.pkl', 'rb') as fin:
    print("Model Loaded")
    model = pickle.load(fin)

print("Monitor Funtion Initialised")

def monitor(s):
    l=monitorDict[s][-3:]
    extflag = 0
    # print(l)
    if len(l)==2:
        cont = l[0]+""
        # print(cont)
        val = model.score(l[1],cont.split())
        print(val)
    elif len(l)==3:
        cont = l[0]+" "+l[1]
        # print(cont)
        val = model.score(l[2],cont.split())
        print(val)
        if l[2] == '</s>':
            print('User Exited')
            extflag = 1 
    
    if val<0.2:
        return 'Anomaly Detected'
    else:
        if extflag == 1:
            monitorDict[s].clear()
            monitorDict[s].append('<s>')
            print('Values Cleared')
        return 'Normal Movement'







print('All other MQTT funtions Initialised')

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client,msg):   
    time.sleep(1)
    # msg = f"messages: {msg_count}"
    topic1="sensors/control/monitored"
    result = client.publish(topic1, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic1}`")
    else:
        print(f"Failed to send message to topic {topic1}")
    if msg.split(" ")[0] == 'Anomaly':
        topic2="sensors/control/monitored/anomaly"
        result = client.publish(topic2, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic2}`")
        else:
            print(f"Failed to send message to topic {topic2}")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        s=msg.payload.decode()
        print(f"Received `{s}` from `{msg.topic}` topic")
        s=s.split(",")
        if s[1] not in monitorDict:
            monitorDict[s[1]]=[]
            monitorDict[s[1]].append("<s>") 
            monitorDict[s[1]].append(s[0])
            mess = monitor(s[1]) + " current position : " + s[0] 
            publish(client, mess)  
            print(mess)   
        elif monitorDict[s[1]][-1:][0] != s[0]:
            print(monitorDict[s[1]][-1:][0], " !!! ", s[0] )
            monitorDict[s[1]].append(s[0])
            mess = monitor(s[1]) + " current position : " + s[0]
            publish(client, mess)
            print(mess)
        # print(monitorDict)
    

    client.subscribe(topic)
    client.on_message = on_message

monitorDict={}
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()