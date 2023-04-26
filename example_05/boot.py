try:
  import usocket as socket
except:
  import socket

import machine
import network

import gc
gc.collect()

from credentials import credentials

station = network.WLAN(network.AP_IF)

station.active(True)
station.config(essid=credentials.get_ssid(), password=credentials.get_password())

while station.active() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = machine.Pin(2, machine.Pin.OUT)
