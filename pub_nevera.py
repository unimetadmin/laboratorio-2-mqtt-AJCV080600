import sys
import json
import time
import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import datetime

def on_connect(client, userdata, flags, rc):
    print('Conectado')

def main():
    client = paho.mqtt.client.Client("Nevera", False)
    client.qos = 0
    client.connect(host='localhost')

    hora1 = hora2 = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

    while True:
        hora1 = hora1 + datetime.timedelta(minutes=5)
        hora2 = hora2 + datetime.timedelta(minutes=10)
        temp = round(np.random.normal(10, 2), 2)
        hielo = int(np.random.uniform(0, 10))

        payload1 = {
            "fecha": str(hora1),
            "temperatura_nevera": str(temp)
        }

        payload2 = {
            "fecha": str(hora2),
            "hielo": str(hielo)
        }

        client.publish("casa/cocina/temperatura_nevera", json.dumps(payload1), qos=0)
        client.publish("casa/cocina/temperatura_nevera", json.dumps(payload2), qos=0)

        print(payload1)
        print(payload2)

        time.sleep(0.5)

if __name__ == "__main__":
    main()
    sys.exit(0)