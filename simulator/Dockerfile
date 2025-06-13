FROM python:3.11-slim
WORKDIR /app
COPY sensor_simulator.py processing_node.py ./
RUN pip install --no-cache-dir paho-mqtt requests
CMD ["python", "sensor_simulator.py"]
