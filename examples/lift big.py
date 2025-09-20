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
        # End-Stop Bottom
        # board.GP4, # NO
        board.GP5,  # NC
        # End-Stop TOP
        # board.GP16, # NO
        board.GP17,  # NC
    ),
    value_when_pressed=False,
    pull=True,
)

BOARD_GP20 = 0
BOARD_GP21 = 1
GROVE_DUAL_1 = 2
GROVE_DUAL_2 = 3
ENDSTOP_BOTTOM = 4
ENDSTOP_TOP = 5


# servo setup
pwm1 = pwmio.PWMOut(board.GP12, duty_cycle=0, frequency=50)
servo1 = servo.Servo(pwm1, min_pulse=501, max_pulse=2540, actuation_range=180)

SERVO_POS_TOP = 0
SERVO_POS_BOTTOM = 180
angle = SERVO_POS_BOTTOM
servo1.angle = SERVO_POS_BOTTOM


import pwmio
from adafruit_motor import motor

# DC motor setup
PWM_M1A = board.GP8
PWM_M1B = board.GP9
M1A = pwmio.PWMOut(PWM_M1A, frequency=10000)
M1B = pwmio.PWMOut(PWM_M1B, frequency=10000)
motor1 = motor.DCMotor(M1A, M1B)


def handleButtons():
    global angle

    event = keys.events.get()
    if event and event.pressed:
        # angle_target = angle
        if event.key_number == BOARD_GP20:
            print("motor +")
            motor1.throttle = 0.5
        if event.key_number == BOARD_GP21:
            print("motor -")
            motor1.throttle = -0.5
        # Limit the angle from 0 to 180 degrees.
        # if angle_target > 180:
        #     angle_target = 180
        # if angle_target < 0:
        #     angle_target = 0

        #  DUAL BUTTON
        if event.key_number == GROVE_DUAL_2:
            print("ping")
            # angle_target = SERVO_POS_TOP
        # if event.key_number == 3:
        #     angle_target = SERVO_POS_RIGHT

        if event.key_number == ENDSTOP_BOTTOM:
            print("ENDSTOP_BOTTOM")
            motor1.throttle = 0
        if event.key_number == ENDSTOP_TOP:
            print("ENDSTOP_TOP")
            motor1.throttle = 0

    #  while angle != angle_target:
    #             if angle < angle_target:
    #                 angle += 1
    #             else:
    #                 angle -= 1
    #             servo1.angle = angle
    #             time.sleep(0.04)
    #         time.sleep(1)
    #         angle = SERVO_POS_BOTTOM
    #         servo1.angle = angle
    #         time.sleep(1)

def main():
    handleButtons()


while True:
    main()
