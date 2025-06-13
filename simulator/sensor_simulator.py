import os
import time
import json
import random
from datetime import datetime
import paho.mqtt.publish as publish

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
CONTAINER_ID = os.getenv("CONTAINER_ID", "contenedor_1")

while True:
    payload = {
        "nivel": random.randint(0, 100),
        "temp": random.randint(10, 50),
        "gases": random.randint(0, 100),
        "timestamp": datetime.utcnow().isoformat(),
        "container_id": CONTAINER_ID
    }
    publish.single(f"sensors/{CONTAINER_ID}", json.dumps(payload), hostname=MQTT_HOST)
    time.sleep(300)
