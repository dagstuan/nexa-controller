from datetime import datetime
import RPi.GPIO as GPIO
import time

pin_to_use = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_to_use, GPIO.OUT)

def delay_microseconds(microseconds):
  time.sleep(microseconds/1000000.)

def send_encoded_bit(gpio_pin, bit):
  if bit:
    GPIO.output(gpio_pin, True)
    delay_microseconds(250)
    GPIO.output(gpio_pin, False)
    delay_microseconds(1250)
  else:
    GPIO.output(gpio_pin, True)
    delay_microseconds(250)
    GPIO.output(gpio_pin, False)
    delay_microseconds(250)

def send_bit(gpio_pin, bit):
  send_encoded_bit(gpio_pin, bit)
  send_encoded_bit(gpio_pin, not bit)

def send_nexa_message(gpio_pin, transmitter_id, recepient, on_off, dimmer_level = -1):
  print(f'setting switch {recepient} to {on_off} and dimmer level {dimmer_level} with transmitter_id {transmitter_id}')

  binary_transmitter_id = format(transmitter_id, '026b')
  binary_recepient = format(recepient, '004b')

  # latch sequence
  GPIO.output(gpio_pin, True)
  delay_microseconds(250)
  GPIO.output(gpio_pin, False)
  delay_microseconds(2500)

  # Send transmitter ID
  for bit in binary_transmitter_id:
    send_bit(gpio_pin, bit == '1')

  # Send group bit
  send_bit(gpio_pin, False)

  # Dimmer level or on off bit (on = 0, off = 1)
  if dimmer_level >= 0:
    send_encoded_bit(gpio_pin, False)
    send_encoded_bit(gpio_pin, False)
  else:
    send_bit(gpio_pin, on_off)

  # 4 bits for receipent
  for bit in binary_recepient:
    send_bit(gpio_pin, bit == '1')

  # Done with command, send pause
  GPIO.output(gpio_pin, True)
  delay_microseconds(250)
  GPIO.output(gpio_pin, False)
  delay_microseconds(10000)

remote_id = 38309186

for x in range(0,5):
  send_nexa_message(pin_to_use, remote_id, 0, True)

GPIO.output(pin_to_use, True)
GPIO.cleanup()
