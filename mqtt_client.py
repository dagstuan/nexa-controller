import paho.mqtt.client as mqtt
import nexa_switcher
import math
from decouple import config

gpio_pin_to_use = int(config('GPIO_PIN'))
remote_id = int(config('REMOTE_ID'))
repeats = int(config('REPEATS'))

host = config('MQTT_HOST')
port = int(config('MQTT_PORT'))
username = config('MQTT_USERNAME')
password = config('MQTT_PASSWORD')

print("Will use GPIO pin ", gpio_pin_to_use, "to communicate. Remote id: ", remote_id, ". Repeats: ", repeats)
print("Will publish to ", host, " with port ", port)

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
    client.publish(state_topic_spots, payload, retain=True)

  if (message.topic == command_topic_oy):
    on_off_state = payload == payload_on
    dimmer_level = 15 if on_off_state else -1

    toggle_light(light_id_oy, on_off_state, dimmer_level)
    client.publish(state_topic_oy, payload, retain=True)

  if (message.topic == brightness_command_topic_spots):
    dimmer_level = math.floor(15/255 * int(payload))

    if (dimmer_level == 0):
      turn_off_light(light_id_spots, state_topic_spots)
    else:
      toggle_light(light_id_spots, True, dimmer_level)
      client.publish(brightness_state_topic_spots, payload, retain=True)
      client.publish(state_topic_spots, payload_on, retain=True)

  if (message.topic == brightness_command_topic_oy):
    dimmer_level = math.floor(15/255 * int(payload))

    if (dimmer_level == 0):
      turn_off_light(light_id_oy, state_topic_oy)
    else:
      toggle_light(light_id_oy, True, dimmer_level)
      client.publish(brightness_state_topic_oy, payload, retain=True)
      client.publish(state_topic_oy, payload_on, retain=True)

def turn_off_light(light_id, state_topic):
  toggle_light(light_id, False, -1)
  client.publish(state_topic, payload_off, retain=True)

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
