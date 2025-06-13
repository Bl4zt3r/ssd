import os
import json
import psycopg2
from fastapi import FastAPI
import paho.mqtt.publish as publish

app = FastAPI()

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "sced")
DB_USER = os.getenv("POSTGRES_USER", "sced_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "securepass")


def get_conn():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)


@app.post("/api/report")
async def report(payload: dict):
    publish.single("backend/data", json.dumps(payload), hostname=MQTT_HOST)
    return {"status": "ok"}


@app.get("/api/contenedores")
def contenedores():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nivel, temp, gases, fecha FROM mediciones ORDER BY fecha DESC LIMIT 100")
        rows = cur.fetchall()
    data = [
        {"id": r[0], "nivel": r[1], "temp": r[2], "gases": r[3], "fecha": r[4].isoformat()} for r in rows
    ]
    return data
