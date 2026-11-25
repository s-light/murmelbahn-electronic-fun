import time
import board
import digitalio
import pwmio
from adafruit_motor import servo

print("example: servo.py")


import keypad

keys = keypad.Keys(
    (
        # onboard buttons
        board.GP20,
        board.GP21,
        # GROVE dual Button on `GROVE 2` port.
        board.GP2,
        board.GP3,
    ),
    value_when_pressed=False,
    pull=True,
)


# servo setup
pwm1 = pwmio.PWMOut(board.GP12, duty_cycle=0, frequency=50)
servo1 = servo.Servo(pwm1, min_pulse=501, max_pulse=2540, actuation_range=180)

SERVO_POS_LEFT = 0
SERVO_POS_RIGHT = 180


angle = 0

def main():
    global angle

    event = keys.events.get()
    # event will be None if nothing has happened.
    # if event:
    #     print(event)
    if event and event.pressed:
        if event.key_number == 0:
            angle_target += 5
        if event.key_number == 1:
            angle_target -= 5
        if event.key_number == 2:
            angle_target = SERVO_POS_LEFT
        if event.key_number == 3:
            angle_target = SERVO_POS_RIGHT

        # Limit the angle from 0 to 180 degrees.
        if angle_target > 180:
            angle_target = 180
        if angle_target < 0:
            angle_target = 0

        while angle != angle_target:
            if angle < angle_target:
                angle += 1
            else:
                angle -= 1
            servo1.angle = angle
            time.sleep(0.05)


while True:
    main()
