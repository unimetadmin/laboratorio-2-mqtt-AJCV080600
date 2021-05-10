import sys
import paho.mqtt.client
import psycopg2
import json

def on_connect(client, userdata, flags, rc):
	print('Conectado (%s)' % client._client_id)
	client.subscribe(topic='casa/#', qos=2)

def on_message(client, userdata, message):
	try:
		connection = psycopg2.connect(
			host='queenie.db.elephantsql.com',
			user='fwtwoqbi',
			password='2xJJGMcXtG9dbW_LQt180KMWkc41_tqM',
			database='fwtwoqbi'
		)
		cursor = connection.cursor()
		msg = json.loads(message.payload)

		print(msg)

		if (msg.get("temperatura_nevera")):
			cursor.execute("""
			INSERT INTO nevera (tipo_reporte, valor, fecha)
			VALUES (%s, %s, %s);""", ["temperatura", msg["temperatura_nevera"], msg["fecha"]])
			connection.commit()
		elif (msg.get("hielo")):
			cursor.execute("""
			INSERT INTO nevera (tipo_reporte, valor, fecha)
			VALUES (%s, %s, %s);""", ["hielo", msg["hielo"], msg["fecha"]])
			connection.commit()
		elif (msg.get("temperatura_olla")):
			cursor.execute("""
			INSERT INTO olla (temperatura, fecha)
			VALUES (%s, %s);""", [msg["temperatura_olla"], msg["fecha"]])
			connection.commit()
			if (msg.get("alerta")):
				cursor.execute("""
				INSERT INTO alerta (mensaje, fecha)
				VALUES (%s, %s);""", [msg["alerta"], msg["fecha"]])
				connection.commit()
		elif (msg.get("cantidad_personas")):
			cursor.execute("""
			INSERT INTO contador (personas, fecha)
			VALUES (%s, %s);""", [msg["cantidad_personas"], msg["fecha"]])
			connection.commit()
			if (msg.get("alerta")):
				cursor.execute("""
				INSERT INTO alerta (mensaje, fecha)
				VALUES (%s, %s);""", [msg["alerta"], msg["fecha"]])
				connection.commit()
		elif (msg.get("temperatura_ccs")):
			cursor.execute("""
			INSERT INTO alexa (temperatura, fecha)
			VALUES (%s, %s);""", [msg["temperatura_ccs"], msg["fecha"]])
			connection.commit()
		elif (msg.get("nivel_tanque")):
			cursor.execute("""
			INSERT INTO tanque (nivel, fecha)
			VALUES (%s, %s);""", [msg["nivel_tanque"], msg["fecha"]])
			connection.commit()
			if (msg.get("alerta")):
				cursor.execute("""
				INSERT INTO alerta (mensaje, fecha)
				VALUES (%s, %s);""", [msg["alerta"], msg["fecha"]])
				connection.commit()

	except(Exception, psycopg2.Error) as e:
		print(f"No se pudo conectar a la base de datos: {e}")
	
	finally:
		if connection:
			cursor.close()
			connection.close()


def main():
	client = paho.mqtt.client.Client(client_id='Casa', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='localhost', port=1883)
	client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)