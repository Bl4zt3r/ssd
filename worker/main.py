import os
import json
import psycopg2
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "sced")
DB_USER = os.getenv("POSTGRES_USER", "sced_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "securepass")


def get_conn():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)


def on_connect(client, userdata, flags, rc):
    client.subscribe("backend/data")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        return
    required = {"nivel", "temp", "gases", "timestamp"}
    if not required.issubset(data.keys()):
        return
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO mediciones (contenedor_id, nivel, temp, gases, fecha) VALUES (%s, %s, %s, %s, NOW())",
            (data.get("container_id", 1), data["nivel"], data["temp"], data["gases"]),
        )
        conn.commit()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, 1883, 60)
client.loop_forever()
