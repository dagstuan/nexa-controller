# Pi Nexa Controller

This project describes the controller I use to control my kitchen lights at home. I use a
cheap 433mhz transmitter connected to my Raspberry pi to control nexa kitchen lights in home assistant.

This project connects to an MQTT broker and communicates with HASS through it.

# Setup

Run `./setup.sh` to set up a docker container connecting to the MQTT broker. The script also expects
to find a file called `config.cfg` that contains relevant configuration. A sample `config.cfg` can be found below.

```
[config]
gpio_pin = 17 # GPIO pin to use. Normally the transmitter is connected to port 17
remote_id = [remote_id] # int remote id sniffed from 433 receiver

[mqtt]
host = [host]
port = [port]
username = [username]
password = [password]
```

Home assistant must also be configured to publish/subscribe to the MQTT-broker. A sample setup is found
in `hass-setup.yml`

# Development

The code is written for Python 3. To run the code outside of Docker you need two packages. `rpi.gpio` and `paho-mqtt`

```
pip3 install rpi.gpio
pip3 install paho-mqtt
```

# Demo

A demo of a working setup controlling Nexa lights through Apple HomeKit and Home Assistant can be found here: https://youtu.be/HXku3B9_a_I

# Links

https://www.instructables.com/Super-Simple-Raspberry-Pi-433MHz-Home-Automation/
https://homeeasyhacking.fandom.com/wiki/Advanced_Protocol
https://github.com/henrikjonhed/NexaTransmitterRPi
