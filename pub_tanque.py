import sys
import json
import time
import paho.mqtt.client
import paho.mqtt.publish
from math import ceil
import numpy as np
import datetime

def on_connect(client, userdata, flags, rc):
    print('Conectado')

def main():
    client = paho.mqtt.client.Client("Tanque", False)
    client.qos = 0
    client.connect(host='localhost')

    agua = 100
    hora = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    i = 1

    while True:
        hora = hora + datetime.timedelta(minutes=10)
        level_down = round(np.random.normal(10, 5), 2)
        level_up = round(np.random.normal(20, 5), 2)

        agua -= level_down
        agua = round(agua, 2)

        if (agua < 0):
            agua = 0
        
        payload = {
            "fecha": str(hora),
            "nivel_tanque": str(agua)
        }

        if (agua <= 50):
            if (agua == 0):
                payload = {
                    "fecha": str(hora),
                    "nivel_tanque": str(agua),
                    "alerta": "Tanque vacío"
                }
            else:
                payload = {
                    "fecha": str(hora),
                    "nivel_tanque": str(agua),
                    "alerta": f"Tanque al {ceil(agua)}%"
                }

        if ((i % 3) == 0):
            agua += level_up
            agua = round(agua, 2)

            if (agua > 100):
                agua = 100

            if (agua <= 50):
                payload = {
                    "fecha": str(hora),
                    "nivel_tanque": str(agua),
                    "alerta": f"Tanque al {ceil(agua)}%"
                }
            else:
                payload = {
                    "fecha": str(hora),
                    "nivel_tanque": str(agua)
                }

        client.publish("casa/baño/nivel_tanque", json.dumps(payload), qos=0)

        print(payload)

        time.sleep(0.5)
        i += 1

if __name__ == "__main__":
    main()
    sys.exit(0)