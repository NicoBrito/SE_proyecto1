import Stepper
from machine import Pin, ADC
import time
from weight import Weight

class Motor:

    def __init__(self,in1,in2,in3,in4):
        self.in1 = Pin(in1,Pin.OUT)
        self.in2 = Pin(in2,Pin.OUT)
        self.in3 = Pin(in3,Pin.OUT)
        self.in4 = Pin(in4,Pin.OUT)
        self.s1 = Stepper.create(self.in1,self.in2,self.in3,self.in4, delay=1)

    def spin(self,food = "Mani"):
        weight_sensor = Weight(14, 21,80837)
        while True:
            
            self.s1.step(500,-1)
            
            


