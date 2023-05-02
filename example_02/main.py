from machine import Pin

# Define button pins
mani_button = Pin(35, Pin.IN, Pin.PULL_UP)
almendra_button = Pin(34, Pin.IN, Pin.PULL_UP)

# Example code to read the state of the buttons
while True:
    # Read the state of the buttons
    state_a0 = mani_button.value()
    state_a1 = almendra_button.value()

    # Print the state of the buttons
    print("Button A0:", state_a0)
    print("Button A1:", state_a1)
    