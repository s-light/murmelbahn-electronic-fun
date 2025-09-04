# SPDX-FileCopyrightText: 2025 stefan krüger
# SPDX-License-Identifier: CC0 (PublicDomain)

# react on marble and do things..

import time
import board

import usb_cdc
dataio = usb_cdc.data

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


# sensor
import busio
import adafruit_tcs34725

i2c = busio.I2C(board.GP1, board.GP0)
sensor = adafruit_tcs34725.TCS34725(i2c, address=0x29)

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4

sensor_debounce_start = time.monotonic()

# servo setup
import pwmio
from adafruit_motor import servo

pwm1 = pwmio.PWMOut(board.GP12, duty_cycle=0, frequency=50)
servo1 = servo.Servo(pwm1, min_pulse=500, max_pulse=2500, actuation_range=180)

SERVO_POS_LEFT = 55
SERVO_POS_RIGHT = 10


# leds
import neopixel
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import PURPLE

num_leds = 20
pixels_left = neopixel.NeoPixel(board.GP14, num_leds, brightness=0.5, auto_write=False)
pixels_right = neopixel.NeoPixel(board.GP15, num_leds, brightness=0.5, auto_write=False)

comet_left = Comet(
    pixels_left,
    speed=0.02,
    color=PURPLE,
    tail_length=10,
)

comet_right = Comet(
    pixels_right,
    speed=0.02,
    color=PURPLE,
    tail_length=10,
)

def comet_stop(animation):
    if animation.cycle_count >= 2:
        animation.freeze()
        animation.reset()
        animation.cycle_count = 0


comet_left.add_cycle_complete_receiver(comet_stop)
comet_left.freeze()
comet_right.add_cycle_complete_receiver(comet_stop)
comet_right.freeze()

animation = comet_left

COLOR_STANDBY = (0, 0, 1)
LEFT = True
RIGHT = False
gate_pos = LEFT
gate_pos_old = RIGHT


##########################################

# main

print("murmelbahn-electronic-fun - main.py")


def gate_left_activate():
    servo1.angle = SERVO_POS_LEFT
    comet_left.resume()
    pixels_right.fill(COLOR_STANDBY)
    pixels_right.show()


def gate_right_activate():
    global animation
    servo1.angle = SERVO_POS_RIGHT
    animation.pixels.fill(COLOR_STANDBY)
    animation.pixels.show()
    animation = comet_left
    comet_right.resume()


def gate_switch():
    if gate_pos == LEFT:
        gate_left_activate()
    elif gate_pos == RIGHT:
        gate_right_activate()
    time.sleep(0.1)


def gate_toggle():
    global gate_pos
    if gate_pos == LEFT:
        gate_pos = RIGHT
        print("gate_pos: RIGHT")
    elif gate_pos == RIGHT:
        gate_pos = LEFT
        print("gate_pos: LEFT")


def main():
    global gate_pos
    global gate_pos_old
    global sensor_debounce_start

    event = keys.events.get()
    # event will be None if nothing has happened.
    # if event:
    #     print(event)
    if event and event.pressed:
        if event.key_number == 0:
            gate_pos = RIGHT
        if event.key_number == 1:
            gate_pos = LEFT
        if event.key_number == 2:
            gate_pos = RIGHT
        if event.key_number == 3:
            gate_pos = LEFT


    value = sensor.color_raw[3]
    if ((time.monotonic() - sensor_debounce_start) > 1.0) and value > 13:
        sensor_debounce_start = time.monotonic()
        print("ping! murmel erkannt!")
        gate_toggle()
    print(f"{value};{10+ gate_pos*10};")

    if gate_pos_old is not gate_pos:
        gate_switch()
        gate_pos_old = gate_pos

    comet_left.animate()
    comet_right.animate()


# init


while True:
    main()
