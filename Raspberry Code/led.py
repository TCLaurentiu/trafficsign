import RPi.GPIO as GPIO     
ON, OFF = 1, 0

# simple LED

class Led():
    def __init__(self, pin):
        self.pin = pin
        self.state = OFF
        GPIO.setup(self.pin, GPIO.OUT)

    # turn the LED on
    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = ON

    # turn the LED off
    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = OFF

    # switch the LED from on to off, or off to on
    def switch(self):
        if self.state == ON:
            self.turn_off()
        else:
            self.turn_on()