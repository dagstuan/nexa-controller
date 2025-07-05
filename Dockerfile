FROM arm64v8/python:3.13.5-bookworm

RUN apt-get update
RUN apt-get -y upgrade

WORKDIR /usr/src/app
COPY mqtt_client.py .
COPY nexa_switcher.py .
COPY requirements.txt .

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore -r requirements.txt

LABEL com.centurylinklabs.watchtower.enable="false"

CMD ["python", "-u", "mqtt_client.py"]
