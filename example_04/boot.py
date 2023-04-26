try:
  import usocket as socket
except:
  import socket

import machine
import network

import gc
gc.collect()

from credentials import credentials

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(credentials.get_ssid(), credentials.get_password())

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = machine.Pin(2, machine.Pin.OUT)
