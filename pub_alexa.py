import sys
import json
import time
import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import datetime
import requests

def on_connect(client, userdata, flags, rc):
    print('Conectado')

def main():
    client = paho.mqtt.client.Client("Alexa", False)
    client.qos = 0
    client.connect(host='localhost')

    ciudad = "Caracas,Venezuela"
    api_key = "9564afd802328ec72659ee15179898a7"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&units=metric&appid={api_key}"

    response = requests.get(url).json()
    temp = response["main"]["temp"]

    hora = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

    while True:
        hora = hora + datetime.timedelta(hours=1)
        rand_num = np.random.randint(0, 1 + 1)

        payload = {
            "fecha": str(hora),
            "temperatura_ccs": str(temp)
        }

        client.publish("casa/sala/alexa_echo", json.dumps(payload), qos=0)

        print(payload)

        if (rand_num):
            temp += np.random.randint(0, 1 + 1)
        else:
            temp -= np.random.randint(0, 1 + 1)

        time.sleep(0.5)

if __name__ == "__main__":
    main()
    sys.exit(0)