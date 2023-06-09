class Car():
    # a car has a set of (usually 4) motors
    def __init__(self, motors):
        self.motors = motors

    # set the car speed by setting motor speeds
    def set_speed(self, percent):
        for motor in self.motors:
            motor.set_speed(percent)

    # start the car by getting all motors to go forward
    def start(self):
        for motor in self.motors:
            motor.forward()

    # stop the car by stopping each motors and setting their speeds to 0
    def stop(self):
        for motor in self.motors:
            motor.stop()
            motor.set_speed(0)