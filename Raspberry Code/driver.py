from signs import *
from action import Action, SpeedChangeAction, CarStartAction, CarStopAction, StopIgnoreAction
from signs import get_area

STEPS = 3 # number of steps to change to a speed
CROSSING_STEPS = 3 # number of time steps to wait at a crossing
YIELD_STEPS = 2 # number of time steps to wait at a yield
CLOSENESS_THRESHOLD = 5000 # a sign was only taken into account if its area was larger than this; not used anymore
SLOWDOWN_SPEED = 30 # the speed to which the car slows down when encountering a ROUNDABOUT, BUMPY_ROAD, SPEED_BUMP sign

class Driver():
    def __init__(self, car, speed_10, speed_40, speed_60, initial_speed):
        self.car = car
        self.last_sign = None
        # PWM percents corresponding to 10km, 40km and 60km signs
        self.speeds = {
            SP10: speed_10,
            SP40: speed_40,
            SP60: speed_60
        }
        # when this is set to True, the driver ignores traffic signs
        # when encountering a pedestrian crossing, where the car stops
        # this flags ensures the car doesn't see the sign immediately
        # after caring out the stopping actino
        self.should_ignore = False
        # list of actions the car has to take
        self.actions = []
        self.initial_speed = initial_speed
        self.current_speed = 0
        # how many times the car didn't see a sign after seeing one
        self.none_count = 0

    # start the car and get up to speed
    def drive(self):
        self.actions.append(CarStartAction(self.car, self))
        self.prepare_speed_change(self.initial_speed)

    # changes speed incrementally
    def prepare_speed_change(self, next_speed, withStopIgnore = False):
        current_speed = self.current_speed
        speed_step = (next_speed - current_speed)/STEPS

        for i in range(STEPS):
            base_action = SpeedChangeAction(self.car, self, current_speed + (i + 1) * speed_step)
            # the last action is a StopIgnoreAction, to set should_ignore to False
            if i == STEPS - 1 and withStopIgnore:
                self.actions.append(StopIgnoreAction(self.car, self, base_action))
            else:
                self.actions.append(base_action)
            
    # at a pedestrian crossing we stop the car completely, wait a couple of time steps, and then start it back up
    # and get up to speed
    def prepare_crossing(self):
        self.should_ignore = True
        previous_Speed = self.current_speed
        for _ in range(CROSSING_STEPS):
            self.actions.append(CarStopAction(self.car, self))
        self.current_speed = 0

        self.actions.append(CarStartAction(self.car, self))
        self.prepare_speed_change(previous_Speed, withStopIgnore = True)

    # for signs such as stop, no entry, or forbidden for everything
    # gradually sets the speed to 0
    def prepare_finish(self):
        self.prepare_speed_change(0)

    # Stop the car for a certain number of time steps, and then get back up
    # to the original speed
    def prepare_yield(self):
        self.should_ignore = True
        previous_Speed = self.current_speed
        for _ in range(YIELD_STEPS):
            self.actions.append(CarStopAction(self.car, self))
        self.current_speed = 0

        self.actions.append(CarStartAction(self.car, self))
        self.prepare_speed_change(previous_Speed, withStopIgnore = True)

    # slow down in case of speed bumps, bumpy roads, or roundabout, without actually stopping
    def prepare_slowdown(self):
        self.should_ignore = True
        previous_Speed = self.current_speed
        self.prepare_speed_change(SLOWDOWN_SPEED)
        self.prepare_speed_change(previous_Speed, withStopIgnore = True)

    # called when the car sees a sign
    def see_sign(self, sign_data):

        if self.should_ignore:
            return

        # increment the none_count, or reset it if we see some sign
        if sign_data is None:
            self.none_count += 1
        else:
            self.none_count = 0 

        # didn't see anything, not seeing anything now, no need to do anything
        if sign_data is None and self.last_sign is None:
            return

        # seeing a sign after not seeing anything, we need to record this, to eventually respect the sign
        if sign_data is not None and self.last_sign is None:
            self.last_sign = sign_data
            return

        # seeing no sign after seeing one
        # either the model missed it, or we should act on that sign now
        # we decide which is which, by checking if this event happens twice in a row
        if sign_data is None and self.last_sign is not None:
            if self.none_count == 2:
                self.prepare_actions(self.last_sign)
                self.last_sign = sign_data
                self.none_count = 0
            return

        # if we now see a different sign than last time, we act on the last sign
        if sign_data is not None and self.last_sign is not None:
            box, conf, class_id = sign_data
            last_box, last_conf, last_class_id = self.last_sign
            if class_id != last_class_id:
                self.prepare_actions(self.last_sign)
                self.last_sign = sign_data

    # call the appropriate methods for each possible signs
    # to prepare the necessary list of actions
    def prepare_actions(self, sign_data):
        if sign_data is None:
            return
        self.actions = []
        box, conf, sign_id = sign_data
        xmin, ymin, xmin, xmax = box[0], box[1], box[2], box[3]

        if sign_id in [SP10, SP40, SP60]:
            self.prepare_speed_change(self.speeds[sign_id])

        if sign_id == CROSSING:
            self.prepare_crossing()

        if sign_id in [STOP, FORBIDDEN, NO_ENTRY]:
            self.prepare_finish()

        if sign_id == YIELD:
            self.prepare_yield()

        if sign_id in [ROUNDABOUT, BUMPY_ROAD, SPEED_BUMP]:
            self.prepare_slowdown()
            
    # do an action, if any are available, then remove it from the list
    def do_action(self):
        if len(self.actions) == 0:
            return
        self.actions[0].do()
        self.actions.pop(0)

    # stop the car, emptying the action list
    def stop(self):
        self.actions = []
        self.car.stop()
        self.current_speed = 0