import Stepper
from machine import Pin, ADC
import time
 

def motor():
    In1 = Pin(32,Pin.OUT)
    In2 = Pin(33,Pin.OUT)
    In3 = Pin(14,Pin.OUT)
    In4 = Pin(21,Pin.OUT)
    infrarouge = ADC(Pin(34))
    s1 = Stepper.create(In1,In2,In3,In4, delay=1)
    while True:
        s1.step(500) # rotate the stepper motor clockwise
        #s1.step(500,-1) # rotate the stepper motor anti-clockwise

#    def pesa():
#    pass



motor() #Despues pasar parametros del PESO y MODO DE FRUTO SECO motor(peso,modo)
#pesa()