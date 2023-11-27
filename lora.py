import paho.mqtt.client as mqtt
import json
import base64

class MQTTSubscriber:

    def __init__(self, host, port, user_in, password_in):
        self.mqttc_ = mqtt.Client()
        self.mqttc_.on_message = self.onMessage
        self.mqttc_.username_pw_set(user_in, password=password_in)
        self.host_ = host
        self.port_ = port
        self.topics_ = {}
        self.starded_ = False

    def start(self):
        self.mqttc_.connect(self.host_, self.port_)
        for topic in self.topics_:
            self.mqttc_.subscribe(topic, 0)
        self.mqttc_.loop_start()
        self.starded_ = True
    
    def stop(self):
        self.mqttc_.loop_stop()
        self.mqttc_.disconnect()
        self.starded_ = False

    def addSubscription(self, topic, callback_function):
        self.topics_[topic] = callback_function
        if self.starded_:
            self.mqttc_.subscribe(topic, 0)
    
    def onMessage(self, mqttc_in, userdata_in, msg_in):
        self.topics_[msg_in.topic](msg_in.payload)
        
def onNewMessageCB( payload):
        json_str = payload.decode()
        json_rx = json.loads(json_str)
        data = json_rx['data']
        data_hex = base64.b64decode(data).hex()
        # if (len(data_hex) != (2 * self.lora_cfgs_.payload_count)):
        #     print("Payload size is incorrect for {}".format(self.board_id_))
        # n = 2
        # data_hex_list = [data_hex[i:i+n] for i in range(0, len(data_hex), n)]

        # self.updateDataFromLoRa(data_hex_list)

    