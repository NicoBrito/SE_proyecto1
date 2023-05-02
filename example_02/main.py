from machine import Pin
import utime
import time 
#from motor import Motor
import Stepper

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
        calibration_factor =138/494881
        # Convert the raw data to a weight using the calibration factor
        weight = data * calibration_factor
        
        return weight
    

class Motor:

    def __init__(self,in1,in2,in3,in4):
        self.in1 = Pin(in1,Pin.OUT)
        self.in2 = Pin(in2,Pin.OUT)
        self.in3 = Pin(in3,Pin.OUT)
        self.in4 = Pin(in4,Pin.OUT)
        self.s1 = Stepper.create(self.in1,self.in2,self.in3,self.in4, delay=1)

    def spin(self, food="Mani"):
        while True:
            self.s1.step(100, -1)


weight_sensor = Weight(14, 21)
motor = Motor(33, 15, 27, 12)
mani_button = Pin(32, Pin.IN, Pin.PULL_UP)
almendra_button = Pin(13, Pin.IN, Pin.PULL_UP)


food = "nada"
weight_asked = 1000 # 113.1
while True:
    a = weight_sensor.get_weight()
    print(a)
    if a >= weight_asked:
        break  # exit the loop
    else:
        print("Weight: ", a)
        motor.s1.step(100,-1)
        if mani_button.value() == 0:
            food = "Mani"
            print("Current food:", food)
            
            weight_asked = 86.6 #50 gramos
        elif almendra_button.value() == 0:
            food = "Almendra"
            print("Current food:", food)
            weight_asked = 102.0062 #80 gramos

