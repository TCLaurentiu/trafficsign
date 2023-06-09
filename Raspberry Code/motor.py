import RPi.GPIO as GPIO          
from time import sleep
class Motor():
    # a motor controller is able to operate 2 motors
    # we need to provide a PWM signal to the enablePin to control the motor speed
    # in1Pin and in2Pin set the direction of the motor:
    # 0 0 -> motor off
    # 0 1 -> forward
    # 1 0 -> backward
    # if the motor was connected the wrong way, we set isOpposite to True
    def __init__(self, enablePin, in1Pin, in2Pin, isOpposite = False):
        self.enablePin = enablePin
        self.in1Pin = in1Pin
        self.in2Pin = in2Pin
        self.isOpposite = isOpposite
        self.setup_pins()
        self.setup_pwm()
        self.stop()

    # set both in pins to LOW to stop the motor
    def stop(self):
        GPIO.output(self.in1Pin, GPIO.LOW)
        GPIO.output(self.in2Pin, GPIO.LOW)
    
    # initialize pwm
    def setup_pwm(self):
        self.pwm=GPIO.PWM(self.enablePin,1000)
        self.pwm.start(25)

    # all pins are output pins
    def setup_pins(self):
        GPIO.setup(self.enablePin,GPIO.OUT)
        GPIO.setup(self.in1Pin,GPIO.OUT)
        GPIO.setup(self.in2Pin,GPIO.OUT)

    # go forward, depending on what forward means in the case of this motor
    def forward(self):
        if self.isOpposite:
            GPIO.output(self.in1Pin, GPIO.LOW)
            GPIO.output(self.in2Pin, GPIO.HIGH)
        else:
            GPIO.output(self.in1Pin, GPIO.HIGH)
            GPIO.output(self.in2Pin, GPIO.LOW)

    # set motor speed by changing PWM duty cycle
    def set_speed(self, percent):
        self.pwm.ChangeDutyCycle(percent)


GPIO.setmode(GPIO.BCM)
