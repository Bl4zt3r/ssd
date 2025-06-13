"""Basic system test placeholders."""
import os
import time
import json
import paho.mqtt.publish as publish
import requests

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def test_flow():
    payload = {"nivel": 50, "temp": 25, "gases": 20, "timestamp": "test", "container_id": "test"}
    publish.single("sensors/test", json.dumps(payload), hostname=MQTT_HOST)
    time.sleep(5)
    r = requests.get(f"{BACKEND_URL}/api/contenedores")
    assert r.status_code == 200
