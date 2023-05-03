from machine import Pin
import utime
import time 
#from motor import Motor
import Stepper
from hcsr04 import HCSR04

# ------------------ CLASSES ------------------
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
# ----------------------------------------------

# -----------------BOOTING----------------------
# PIN motor/weight
weight_sensor = Weight(26, 27)
motor = Motor(19, 18, 5, 17)
# PIN food
mani_button = Pin(25, Pin.IN, Pin.PULL_UP)
almendra_button = Pin(33, Pin.IN, Pin.PULL_UP)
nuez_button = Pin(32, Pin.IN, Pin.PULL_UP)
#PIN start
start_button = Pin(15, Pin.IN, Pin.PULL_UP) 
# PIN dist
dist_sensor = HCSR04(trigger_pin=2, echo_pin=35, echo_timeout_us=10000)
led_green = Pin(16, Pin.OUT)
led_red = Pin(4, Pin.OUT)
# VAL
food = "nada"
weight_asked = 1000 
print(weight_sensor.get_weight()) 
first_weight = weight_sensor.get_weight()
print("First Weight: ", first_weight)
on = 1
# ----------------------------------------------
while True:
    print("esperando")
    time.sleep(0.3)
    on = start_button.value()
    if on == 0:

        while True:
            #---------LED PROXIMITY SENSOR----------------
            distance = dist_sensor.distance_cm()
            print('Distance:', distance, 'cm')
            if distance < 10: #Valor a cambiar segun "estanque"   
                led_red.value(0)
                led_green.value(1)
            else:
                led_red.value(1)
                led_green.value(0)
            #--------------------------------------------

            #---------- LEER BOTONES --------------------
            time.sleep(0.01)
            first_weight_changed = weight_sensor.get_weight()
            print("Box weight: ", first_weight_changed)
            if mani_button.value() == 0:
                food = "mani"
                objective = 84.6
                break
            elif almendra_button.value() == 0:
                food = "almendra"
                objective = 100.4
                break
            elif nuez_button.value()== 0:
                food = "nuez"
                objective = 107.133
                break 
        # ----------------------------------------------

        # -----------CALCULA EL OFFSET DEL BOWL----------------
        w = first_weight_changed - first_weight 
        print("W es: ", w)
        print("SE PIDE ESTA COMIDA: ", food," que debe pesar ", objective," y con el bowl: ", objective+w)
        objective += w
        out = 0
        # -----------------------------------------------------

        while True:
            #---------LED SENSOR DISTANCIA----------------
            distance = dist_sensor.distance_cm()
            print('Distance:', distance, 'cm')
            if distance < 17.6:
                led_red.value(0)
                led_green.value(1)
            else:
                led_red.value(1)
                led_green.value(0)
            #--------------------------------------------
            
            # ---------LEER PESO MOVER MOTOR-------------------------
            for i in range(2): # Rotate forward two times
                a = weight_sensor.get_weight()
                print("Weight: ",a)
                if (a) >= objective:
                    print("PESO FINAL: ", a)
                    out = 1
                    break  # exit the loop
            if out == 1:
                break    
            else:
                motor.s1.step(100,-1)
            if out == 1:
                break
            motor.s1.step(55, 1) 
            # -------------------------------------------------------