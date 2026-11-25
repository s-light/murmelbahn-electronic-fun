# SPDX-FileCopyrightText: 2025 stefan krüger
# SPDX-License-Identifier: CC0 (PublicDomain)

# stream filtered sensor data for plotting

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

from ExponentialMovingAverage import ExponentialMovingAverage

ema_filter = ExponentialMovingAverage(alpha=0.5)

event_threshold = 5


event = 0

while True:
    color_raw = sensor.color_raw
    color_filtered = ema_filter.update(color_raw)
    if color_filtered[3] > event_threshold:
        event = 20
    else:
        event = 0

    print(
        f"{color_raw[0]};{color_raw[1]};{color_raw[2]};{color_raw[3]};{color_filtered[3]:.2f};{0};{event};"
    )
