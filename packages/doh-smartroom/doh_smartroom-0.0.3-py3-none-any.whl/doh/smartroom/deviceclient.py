import paho.mqtt.client as mqtt
import json 

class DeviceClient(mqtt.Client):
    def __init__(self, device_info, auto_reconnect=True):
        mqtt.Client.__init__(self)
        self.name = device_info["deviceInfo"]['name']
        self.device_info = device_info
        self.auto_reconnect = auto_reconnect
        self.will_set('/outbox/%s/lwt' % self.name, 'anythinghere', 0, False)

    def on_connect(self, client, userdata, flags, rc):
        print('connected')
        self.subscribe("/inbox/%s/deviceInfo" % self.name)
        
        for address in self.device_info["deviceInfo"]["endPoints"]:
            client.subscribe("/inbox/%s/%s" % (self.name, address))

        self.publish("/outbox/%s/deviceInfo" % self.name, json.dumps(self.device_info)) #for autoreconnect


    def on_message(self, userdata, msg):
        print(msg.topic + ": " + str(msg.payload))
        _, box, name , address = msg.topic.split("/")

        if box == "inbox" and str(msg.payload) == "get" and address == "deviceInfo":
            self.publish("/outbox/%s/deviceInfo" % self.name, json.dumps(self.device_info))
            return

        if box == "inbox":
            # echo back
            self.publish("/outbox/%s/%s" % (self.name, address), str(msg.payload))

    def on_disconnect(self, userdata, rc): 
        if rc != 0:
            print("Broker disconnection")

        if self.auto_reconnect:
            time.sleep(10)
            self.connect(mqttBrokerName, mqttBrokerPort, 60)

if __name__ == "__main__":
    dev_info = {'deviceInfo': {'name': 'test', 'endPoints': {'testednpoint1': {}, 'testednpoint2': {}}}}
    dev = DeviceClient(dev_info)
    dev.connect('127.0.0.1', 1883)
    dev.loop_forever()
