# the reaction to seeing a traffic sign is a list of actions
# every action has a __init__ method, from which it takes all the 
# necessary parameters
# all actions receiver the car and the driver instance
# the do method is called whenever the action actually takes places
class Action():
    def __init__(self, car, driver):
        self.car = car
        self.driver = driver
    
    def do(self):
        pass

# speed change action
class SpeedChangeAction(Action):
    def __init__(self, car, driver, new_speed):
        super().__init__(car, driver)
        self.new_speed = new_speed

    # change the car speed, and inform the driver
    def do(self):
        self.car.set_speed(self.new_speed)
        self.driver.current_speed = self.new_speed

# starting the car action
class CarStartAction(Action):
    def __init__(self, car, driver):
        super().__init__(car, driver)
    
    # start the car, and set the speed to 0
    def do(self):
        self.car.start()
        self.driver.current_speed = 0

# stop the car action
class CarStopAction(Action):
    def __init__(self, car, driver):
        super().__init__(car, driver)

    # stop the car, and set its speed to 0
    def do(self):
        self.car.stop()
        self.driver.current_speed = 0

# this actions wraps any normal action, and sets should_ignore to False after caring out the action
class StopIgnoreAction(Action):
    def __init__(self, car, driver, action):
        super().__init__(car, driver)
        self.action = action

    def do(self):
        self.action.do()
        self.driver.should_ignore = False