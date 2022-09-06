import paho.mqtt.client as mqtt
import nexa_switcher
import math

import configparser

config = configparser.ConfigParser()
config.read_file(open(r'config.cfg'))

gpio_pin_to_use = int(config.get('config', 'gpio_pin'))
remote_id = int(config.get('config', 'remote_id'))
repeats = int(config.get('config', 'repeats'))

host = config.get('mqtt', 'host')
port = int(config.get('mqtt', 'port'))
username = config.get('mqtt', 'username')
password = config.get('mqtt', 'password')

light_id_spots = 0 # Id in Nexa
state_topic_spots = "kjokken/spots/status"
command_topic_spots = "kjokken/spots/switch"
brightness_state_topic_spots = "kjokken/spots/brightness"
brightness_command_topic_spots = "kjokken/spots/brightness/set"

light_id_oy = 1 # Id in Nexa
state_topic_oy = "kjokken/oy/status"
command_topic_oy = "kjokken/oy/switch"
brightness_state_topic_oy = "kjokken/oy/brightness"
brightness_command_topic_oy = "kjokken/oy/brightness/set"

payload_on = "ON"
payload_off = "OFF"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  if rc==0:
    print("connected OK Returned code=",rc)
  else:
    print("Bad connection Returned code=",rc)

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("kjokken/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
  payload = str(message.payload.decode("utf-8"))
  print("message received " ,payload)
  print("message topic=",message.topic)

  if (message.topic == command_topic_spots):
    on_off_state = payload == payload_on
    dimmer_level = 15 if on_off_state else -1

    toggle_light(light_id_spots, on_off_state, dimmer_level)
    client.publish(state_topic_spots, payload)

  if (message.topic == command_topic_oy):
    on_off_state = payload == payload_on
    dimmer_level = 15 if on_off_state else -1

    toggle_light(light_id_oy, on_off_state, dimmer_level)
    client.publish(state_topic_oy, payload)

  if (message.topic == brightness_command_topic_spots):
    dimmer_level = math.floor(15/255 * int(payload))

    if (dimmer_level == 0):
      turn_off_light(light_id_spots, state_topic_spots)
    else:
      toggle_light(light_id_spots, True, dimmer_level)
      client.publish(brightness_state_topic_spots, payload)
      client.publish(state_topic_spots, payload_on)

  if (message.topic == brightness_command_topic_oy):
    dimmer_level = math.floor(15/255 * int(payload))

    if (dimmer_level == 0):
      turn_off_light(light_id_oy, state_topic_oy)
    else:
      toggle_light(light_id_oy, True, dimmer_level)
      client.publish(brightness_state_topic_oy, payload)
      client.publish(state_topic_oy, payload_on)

def turn_off_light(light_id, state_topic):
  toggle_light(light_id, False, -1)
  client.publish(state_topic, payload_off)

def toggle_light(light_id, on_off_state, dimmer_level = -1):
  nexa_switcher.switch(gpio_pin_to_use, remote_id, light_id, on_off_state, dimmer_level, repeats)

def on_disconnect(client, userdata, rc):
    print("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True

client = mqtt.Client()

client.username_pw_set(username, password)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(host, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
