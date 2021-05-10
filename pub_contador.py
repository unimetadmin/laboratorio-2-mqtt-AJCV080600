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
    client = paho.mqtt.client.Client("Contador", False)
    client.qos = 0
    client.connect(host='localhost')

    hora = datetime.datetime.today().replace(minute=0, second=0, microsecond=0)

    while True:
        hora = hora + datetime.timedelta(minutes=1)
        personas = int(np.random.uniform(0, 10))

        payload = {
            "fecha": str(hora),
            "cantidad_personas": str(personas)
        }

        if (personas > 5):
            payload = {
                "fecha": str(hora),
                "cantidad_personas": str(personas),
                "alerta": "Hay más de 5 personas en la sala"
            }
        
        client.publish("casa/sala/contador_personas", json.dumps(payload), qos=0)

        print(payload)

        time.sleep(0.5)

if __name__ == "__main__":
    main()
    sys.exit(0)