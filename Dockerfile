FROM arm32v7/python:3

WORKDIR /usr/src/app
COPY mqtt_client.py .
COPY nexa_switcher.py .
COPY config.cfg .

RUN pip install --no-cache-dir rpi.gpio
RUN pip install --no-cache-dir paho-mqtt

CMD ["python", "-u", "mqtt_client.py"]
