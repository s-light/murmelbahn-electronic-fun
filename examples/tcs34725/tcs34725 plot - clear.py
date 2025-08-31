# SPDX-FileCopyrightText: 2025 stefan krüger
# SPDX-License-Identifier: CC0 (PublicDomain)

# stream sensor data for plotting in serial-plot

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

while True:
    value = sensor.color_raw[3]
    print(value)
    if value > 12:
        # marble!
