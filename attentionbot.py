import time

from api import Api
from motors import Servo, Motor
from remote import Remote

servo = Servo(port=1, min_pulse=750, max_pulse=2250, min_position=0.30, max_position=0.7)
motor = Motor(port=1, duty_cycle=0)

def wave(min=0.0, max=1.0, n=1, pause=0.4):
    for x in range(n):
        servo.set(min)
        time.sleep(pause)
        servo.set(max)
        time.sleep(pause)
        servo.set(0.5)

api = Api()
api.demonize()
remote = Remote()

while True:
    # api events
    for event, kwargs in api.events:
        if event == "wave":
            wave(**kwargs)
        if event == "set":
            servo.set(0.75-float(kwargs["position"])*0.5)
        if event == "set_speed":
            motor.duty_cycle = kwargs['position']
    api.events = []


    if not remote.wm:
       motor.tick()
       continue

    # remote events
    if remote.pressed('a'):
        remote.rumble(True)
    else:
        remote.rumble(False)
    print remote.angle()
    if remote.pressed('b'):
        accel = remote.accel()
        steer = accel[0] * -1
        steer = 0.5 if steer > -1 and steer < 1 else (steer + 25)/50.0
        speed = accel[1]
        speed = (speed + 15)/25.0

        servo.set(steer)
        motor.duty_cycle = speed
    else:
        if remote.pressed('left'):
            servo.set(1)
        elif remote.pressed('right'):
            servo.set(0)
        else:
            servo.set(0.5)

        if remote.pressed('up'):
            motor.duty_cycle = 0.1
        else:
            motor.duty_cycle = 0

    if remote.pressed('home'):
        time.sleep(1)
        remote.calibrate()
        remote.rumble(True)
        time.sleep(0.1)
        remote.rumble(False)

    motor.tick()
    #time.sleep(0.01)
