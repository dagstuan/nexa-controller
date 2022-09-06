FROM arm32v7/python:3

RUN apt-get update
RUN apt-get -y upgrade

WORKDIR /usr/src/app
COPY mqtt_client.py .
COPY nexa_switcher.py .
COPY config.cfg .
COPY requirements.txt .

# Fix build of RPi.GPIO
ENV CFLAGS=-fcommon
RUN pip3 install -r requirements.txt

LABEL com.centurylinklabs.watchtower.enable="false"

CMD ["python3", "-u", "mqtt_client.py"]
