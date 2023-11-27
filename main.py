from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import lora as lora
import json
import base64


app = Flask(__name__)
CORS(app)
import struct

def Lat_hex(hex_string):
    
    hex_bytes = bytes.fromhex(hex_string)
    if len(hex_bytes) != 4:
        raise ValueError("A entrada deve ter 4 bytes")

    decimal_valueLat = struct.unpack('>f', hex_bytes)[0]

    return decimal_valueLat

def Lon_hex(hex_string):
    
    hex_bytes = bytes.fromhex(hex_string)

    if len(hex_bytes) != 4:
        raise ValueError("A entrada deve ter 4 bytes")

    decimal_valueLon = struct.unpack('>f', hex_bytes)[0]

    return decimal_valueLon


def onNewMessageCB(payload):
        json_str = payload.decode()
        json_rx = json.loads(json_str)
        data = json_rx['data']
        data_hex = base64.b64decode(data).hex()
        print("Dados hexadecimais recebidos:", data_hex)
        latitude = data_hex[:8]
        longitude = data_hex[-8:]
        global decimal_valueLat
        global decimal_valueLon
        decimal_valueLat = Lat_hex(latitude)
        decimal_valueLon = Lon_hex(longitude)
        print(decimal_valueLon)
        print(decimal_valueLat)
        
# Inicializa comunicação LoRa
mqtt_host = "127.0.0.1"
mqtt_port = 1883
mqtt_user = "JG"
mqtt_pwd = "GAIn123"
subs = lora.MQTTSubscriber(mqtt_host, mqtt_port, mqtt_user, mqtt_pwd)

subs.start()
subs.addSubscription("application/1/device/2232330000888806/rx", onNewMessageCB)
   
@app.route("/gps_data", methods=['GET', 'POST'])
def gps_data():
    if request.method == 'POST':
       
        # Simulando os valores de latitude e longitude
        latitude = decimal_valueLat
        longitude = decimal_valueLon
        
        gps_data = {
            "latitude": latitude,
            "longitude": longitude
        }
        
        return jsonify(gps_data)
    
if __name__ == "__main__":
    host = 'localhost'
    port = 5000
    app.run(host=host, port=port)