import RPi.GPIO as GPIO

# a simple button, connected to 2 RPi pins
# it works by outputing HIGH from one of the pins, and checking if the other received it
class Button():
    def __init__(self, outPin, inPin):
        self.outPin = outPin
        self.inPin = inPin
        self.init_button()

    def init_button(self):
        GPIO.setup(self.outPin, GPIO.OUT)
        GPIO.setup(self.inPin, GPIO.IN)

    def is_pressed(self):
        GPIO.output(self.outPin, GPIO.HIGH)
        pressed = GPIO.input(self.inPin)
        GPIO.output(self.outPin, GPIO.LOW)
        return pressed