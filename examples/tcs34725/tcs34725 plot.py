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

# Main loop reading color and printing it every second.
while True:
    # color_rgb = sensor.color_rgb_bytes
    # human readable
    # print(
    #     f"{color_rgb[0]}; {color_rgb[1]:>3}; {color_rgb[2]:>3}; {sensor.color_temperature:>6.2}; {sensor.lux:>3.2}"
    # )
    # serial-plotter
    # print(
    #     f"{color_rgb[0]};{color_rgb[1]};{color_rgb[2]};{sensor.color_temperature};{sensor.lux}"
    # )
    # color_raw = sensor.color_raw
    # print(f"{color_raw[0]};{color_raw[1]};{color_raw[2]};{color_raw[3]};")
    print(sensor.color_raw[3])

    # mu plotter
    # print(
    #     (color_rgb[0], color_rgb[1], color_rgb[2], sensor.color_temperature, sensor.lux)
    # )
    # time.sleep(0.1)
