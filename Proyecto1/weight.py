from machine import Pin
import utime
import time 
class Weight:
    def __init__(self, pin_dt_num, pin_sck_num, calibration=1):
        self.dt_pin = Pin(pin_dt_num, Pin.IN)
        self.sck_pin = Pin(pin_sck_num, Pin.OUT)
        self.calibration = calibration


    def get_weight(self):
        # Wait for the HX711 to become ready
        while self.dt_pin.value() == 1: 
            pass

        # Create a variable to store the raw 24-bit data
        data = 0

        # Read the raw 24-bit data from the HX711
        for i in range(24):
            self.sck_pin.on()
            time.sleep_us(1)
            data <<= 1
            self.sck_pin.off()
            time.sleep_us(1)
            data |= self.dt_pin.value()

        # Set the channel and gain factor for the next reading
        self.sck_pin.on()
        self.sck_pin.off()

        # Wait for the HX711 to settle
        time.sleep(0.1)
        calibration = 1234.56*(138/216) 
        # Convert the raw data to a weight using the calibration factor
        weight = (float((data ^ 0x800000) - 0x800000) / calibration)  - 71
        
        return weight
    

weight_sensor = Weight(14, 21)
while True:
    weight_sensor.get_weight()








