from camera import init_camera, init_model, run_inference, get_closest_result
from display_library import lcd
from signs import is_valid, get_name, get_area
from button import Button
from motor import Motor
from car import Car
from driver import Driver
from led import Led

# Motivation for the style of coding and usage of loops, if statements etc is the following:
# the inference is the huge bottleneck of the system, which we can't really control
# it would be rather difficult to introduce a worse bottleneck, and not a good usage of our time
# to try to optimize the rest of the code, especially since it is rather simple
# we considered that it is better to write our code somewhat cleanly

OBSERVE, DRIVE = 0, 1

# initializing everything
model = "model.onnx"
camera = init_camera()
detector = init_model(model) 
display = lcd()
car_button = Button(18, 23)
state_led = Led(16)
state_led.turn_off()

# the car has 2 states, observe and drive
# the observe state simply displays the name
# of the closest sign
# drive is our attempt at a self driving car
state = OBSERVE

# the 4 motors
motor_ul = Motor(10, 11, 9)
motor_ur = Motor(26, 5, 6, isOpposite = True)
motor_dl = Motor(20, 27, 22)
motor_dr = Motor(21, 13, 19, isOpposite = True)


car = Car([motor_ul, motor_ur, motor_dl, motor_dr])
driver = Driver(car, 40, 70, 100, 40)

while True:
    
    # change the car state if the change state button is pressed
    if car_button.is_pressed():
        while car_button.is_pressed(): # debouncing
            pass
        if state == DRIVE: # switch to OBSERVE, stop the car and turn led off
            driver.stop()
            state_led.turn_off()
        else:             # switch to DRIVE; Reinitialize car and driver to not have to deal with manually doing that
            car = Car([motor_ul, motor_ur, motor_dl, motor_dr])
            driver = Driver(car, 40, 70, 100, 40)
            driver.drive()
            state_led.turn_on()
        state = 1 - state

    if state == DRIVE: # if in drive state, do the next action
        driver.do_action()
        print(driver.actions)
        print(driver.should_ignore)

    # run inference, and prepare what needs to be displayed on the lcd
    results = run_inference(camera, detector)
    closest_result = get_closest_result(results)
    display.lcd_clear()
    if is_valid(closest_result):    
        name = get_name(closest_result)
        print(get_area(closest_result))
    else:
        name = ""

    # display the speed in the lower right corner, the sign in the upper left corner, filling everything else up with spaces
    name = name + (32 - len(name) - len(str(int(driver.current_speed)))) * " " + str(int(driver.current_speed))
    display.lcd_display_string(name[:16]) # display first 16 characters on the first line
    display.lcd_display_string(name[16:], line = 2) # display last 16 characters on the last line

    if state == OBSERVE:
        continue
    
    # inform the driver of the current sign if in drive mode
    driver.see_sign(closest_result)
