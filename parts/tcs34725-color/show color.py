# SPDX-FileCopyrightText: 2025 stefan krüger
# SPDX-License-Identifier: CC0 (PublicDomain)

# just show the colors on the build in pixel-leds

import time
import board
import busio

import adafruit_tcs34725

i2c = busio.I2C(board.GP1, board.GP0)
sensor = adafruit_tcs34725.TCS34725(i2c)

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4

import neopixel
pixels = neopixel.NeoPixel(board.GP18, 2)

num_leds = 10
pixels_left = neopixel.NeoPixel(board.GP14, num_leds, brightness=0.7, auto_write=True)

color = (5, 0, 1)
pixels.fill(color)
pixels_left.fill(color)
time.sleep(1)
pixels.fill(0)


while True:
    color_raw = sensor.color_raw
    pixels.fill(
        (
            color_raw[0],
            color_raw[1],
            color_raw[2],
        )
    )
    pixels_left.fill(
        (
            color_raw[0],
            color_raw[1],
            color_raw[2],
        )
    )
    print(
        f"{color_raw[0]};{color_raw[1]};{color_raw[2]};{color_raw[3]};{0};{0};{0};"
    )
