import os
import json
import time
import sqlite3
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import requests

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
DB_FILE = "readings.db"

conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS readings (container TEXT, data TEXT, ts REAL)")
conn.commit()


def on_connect(client, userdata, flags, rc):
    client.subscribe("sensors/#")


def on_message(client, userdata, msg):
    container = msg.topic.split("/")[-1]
    cur.execute("INSERT INTO readings VALUES (?, ?, ?)", (container, msg.payload.decode(), time.time()))
    conn.commit()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, 1883, 60)

last_sent = time.time()

while True:
    client.loop(timeout=1.0)
    if time.time() - last_sent > 900:  # every 15 minutes
        cutoff = time.time() - 2 * 86400
        cur.execute("DELETE FROM readings WHERE ts < ?", (cutoff,))
        cur.execute("SELECT container, data FROM readings")
        rows = cur.fetchall()
        summary = {}
        for container, data in rows:
            summary.setdefault(container, []).append(json.loads(data))
        if summary:
            try:
                requests.post(f"{BACKEND_URL}/api/report", json=summary)
            except Exception as e:
                print("Failed to send summary", e)
        last_sent = time.time()
