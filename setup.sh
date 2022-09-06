#/bin/sh

docker container stop nexa-mqtt
docker container rm nexa-mqtt

docker build -t nexa-mqtt .

docker run -d --privileged --restart=always --name nexa-mqtt nexa-mqtt
