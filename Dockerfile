FROM arm32v7/python:3.10.6-bullseye

RUN apt-get update
RUN apt-get -y upgrade

WORKDIR /usr/src/app
COPY mqtt_client.py .
COPY nexa_switcher.py .
COPY config.cfg .
COPY requirements.txt .

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore -r requirements.txt

LABEL com.centurylinklabs.watchtower.enable="false"

CMD ["python", "-u", "mqtt_client.py"]
