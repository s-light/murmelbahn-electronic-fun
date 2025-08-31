# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
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
    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)

    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    # print(f"RGB color as 8 bits per channel int: #{color:02X} or as 3-tuple: {color_rgb}")

    # Read the color temperature and lux of the sensor too.
    temp = sensor.color_temperature
    lux = sensor.lux
    # print(f"Temperature: {temp}K Lux: {lux}\n")

    print(
        f"color: {color_rgb[0]:>3}, {color_rgb[1]:>3}, {color_rgb[2]:>3} Temperature: {temp}K Lux: {lux}"
    )
    # Delay for a second and repeat.
    time.sleep(1.0)
