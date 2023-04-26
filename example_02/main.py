from esp_ble_uart import *
import time

from machine import freq
#freq(160000000)

from hx711 import HX711

driver = HX711(d_out=5, pd_sck=4)

nom = 'ESP32-ble-uart-gcworks'
UUID_UART = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_TX = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_RX = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
val_rx = "12"

uart = Bleuart(nom, UUID_UART, UUID_TX, UUID_RX)
uart.close()

def rcp_rx():
    global val_rx
    if uart.any():
        while uart.any():
          val_rx = uart.read().decode().strip()
          print('sur rx: ', val_rx)               

def env_tx(val_tx):
    uart.write(str(val_tx) + '\n')
    print("tx", val_tx)

while True:
    uart.irq(handler=rcp_rx)
    print((driver.read()-183200)/238)
    env_tx(round(((driver.read()-183200)/238)+15))       # the mesured weight sent to smartphone
    time.sleep_ms(1000)
driver.power_off()