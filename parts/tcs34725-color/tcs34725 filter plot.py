# SPDX-FileCopyrightText: 2025 stefan krüger
# SPDX-License-Identifier: CC0 (PublicDomain)

# stream sensor data for plotting

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


# Create variables for tracking baseline and previous reading
baseline = 0
previous_reading = 0

window_size = 100  # number of readings to calculate moving average over
filter_threshold = 20  # threshold value for fast changes (adjust to your needs)

event = 0

while True:
    color_raw = sensor.color_raw

    # Calculate moving average over a short window (e.g. 5 seconds)
    current_reading = sum(color_raw[3] for _ in range(window_size)) / window_size

    if previous_reading != 0:  # Check if we have at least one reading to compare
        # Track baseline and fire event on fast changes
        if (current_reading - previous_reading) > filter_threshold or (
            previous_reading - current_reading
        ) > filter_threshold:
            print("Fast change detected!")
            event = 20
        else:
            event = 0

    print(
        f"{color_raw[0]};{color_raw[1]};{color_raw[2]};{color_raw[3]};{previous_reading};{current_reading};{event};"
    )
    previous_reading = current_reading
    # time.sleep(0.1)  # Update rate (adjust to your needs)
