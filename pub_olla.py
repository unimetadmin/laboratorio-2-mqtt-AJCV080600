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
    client = paho.mqtt.client.Client("Olla", False)
    client.qos = 0
    client.connect(host='localhost')

    hora = datetime.datetime.today().replace(minute=0, second=0, microsecond=0)

    while True:
        hora = hora + datetime.timedelta(seconds=1)
        temp = round(np.random.uniform(0, 150), 2)

        payload = {
            "fecha": str(hora),
            "temperatura_olla": str(temp)
        }

        if (temp >= 100):
            payload = {
                "fecha": str(hora),
                "temperatura_olla": str(temp),
                "alerta": "El agua está hirviendo"
            }
        
        client.publish("casa/cocina/temperatura_olla", json.dumps(payload), qos=0)

        print(payload)

        time.sleep(0.5)

if __name__ == "__main__":
    main()
    sys.exit(0)