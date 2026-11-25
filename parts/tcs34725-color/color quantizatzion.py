# SPDX-FileCopyrightText: 2025 stefan krüger
# SPDX-License-Identifier: CC0 (PublicDomain)

# color quantization

import time
import board

import usb_cdc

dataio = usb_cdc.data

import busio

import adafruit_tcs34725

i2c = busio.I2C(board.GP1, board.GP0)
sensor = adafruit_tcs34725.TCS34725(i2c)

# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4

import neopixel

pixels_onboard = neopixel.NeoPixel(board.GP18, 2)
num_leds = 20
pixels_left = neopixel.NeoPixel(board.GP14, num_leds, brightness=1.0, auto_write=False)


# Define the color ranges for each category
# COLOR_RANGES = {
#     "red": ((128, 0, 0), (255, 50, 50)),  # Red: R>128, G<50, B<50
#     "orange": ((255, 100, 0), (255, 200, 0)),  # Orange: R>200, G>100, B<50
#     "yellow": ((255, 200, 0), (255, 250, 0)),  # Yellow: R>200, G>150, B<50
#     "green": ((0, 128, 0), (80, 255, 80)),  # Green: G>128, R<80, B<80
#     "green-blue": ((0, 100, 100), (100, 200, 200)),  # Green-Blue: G>100, B>100, R<100
#     "blue": ((50, 0, 255), (150, 50, 255)),  # Blue: B>128, R<100, G<50
#     "violet": ((150, 0, 200), (250, 50, 255)),  # Violet: R>150, B>200, G<50
#     "white": ((200, 200, 200), (255, 255, 255)),  # White: R>200, G>200, B>200
# }
COLOR_RANGES = {
    "white": ((10, 9, 5), (40, 40, 40)),
    "red": ((8, 2, 2), (30, 10, 10)),
    # "orange": ((9, 7, 2), (30, 10, 10)),
    # "yellow": ((9, 9, 2), (30, 30, 10)),
    "green": ((2, 9, 2), (8, 30, 8)),
    "blue": ((2, 3, 4), (8, 9, 30)),
    "violet": ((5, 3, 5), (30, 8, 30)),
}


def classify_color(color):
    for category, (lower_bound, upper_bound) in COLOR_RANGES.items():
        if (
            lower_bound[0] <= color[0] <= upper_bound[0]
            and lower_bound[1] <= color[1] <= upper_bound[1]
            and lower_bound[2] <= color[2] <= upper_bound[2]
        ):
            return category
    return "unknown"


classified_color_old = ""

while True:
    color_raw = sensor.color_raw
    pixels_left.fill(
        (
            color_raw[0],
            color_raw[1],
            color_raw[2],
        )
    )
    pixels_left.show()
    dataio.write(
        f"{color_raw[0]};{color_raw[1]};{color_raw[2]};{color_raw[3]};{0};{0};{0};\n"
    )
    classified_color = classify_color(color_raw)
    if classified_color != classified_color_old:
        classified_color_old = classified_color
        if classified_color != "unknown":
            print(f"Classified color: {classified_color}")
        else:
            print(f"..")
