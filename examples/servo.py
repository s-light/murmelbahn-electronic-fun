import time
import board
import digitalio
import pwmio
from adafruit_motor import servo

print("example: servo.py")

button1 = digitalio.DigitalInOut(board.GP20)
button1.direction = digitalio.Direction.INPUT
button2 = digitalio.DigitalInOut(board.GP21)
button2.direction = digitalio.Direction.INPUT


# servo setup
pwm1 = pwmio.PWMOut(board.GP12, duty_cycle=0, frequency=50)
pwm2 = pwmio.PWMOut(board.GP13, duty_cycle=0, frequency=50)
pwm3 = pwmio.PWMOut(board.GP14, duty_cycle=0, frequency=50)
pwm4 = pwmio.PWMOut(board.GP15, duty_cycle=0, frequency=50)
servo1 = servo.Servo(pwm1, min_pulse=501, max_pulse=2540, actuation_range=180)
servo2 = servo.Servo(pwm2, min_pulse=501, max_pulse=2540, actuation_range=180)
servo3 = servo.Servo(pwm3, min_pulse=501, max_pulse=2540, actuation_range=180)
servo4 = servo.Servo(pwm4, min_pulse=501, max_pulse=2540, actuation_range=180)


angle = 0

def main():
    global angle

    print(angle)
    # Read buttons' values.
    if not button1.value:
        angle += 5
        time.sleep(0.01)
    if not button2.value:
        angle -= 5
        time.sleep(0.01)

    # Limit the angle from 0 to 180 degrees.
    if angle > 180:
        angle = 180
    if angle < 0:
        angle = 0

    # Update servo angles.
    servo1.angle = servo2.angle = servo3.angle = servo4.angle = angle

    # Delay a bit to allow servo to move.
    time.sleep(0.01)


while True:
    main()
