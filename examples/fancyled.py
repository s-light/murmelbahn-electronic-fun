# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple FancyLED example for NeoPixel strip"""

import board
import neopixel

import adafruit_fancyled.adafruit_fancyled as fancy

num_leds = 20

# Declare a 6-element RGB rainbow palette
palette = [
    fancy.CRGB(1.0, 0.0, 0.0),  # Red
    fancy.CRGB(0.5, 0.5, 0.0),  # Yellow
    # fancy.CRGB(0.0, 1.0, 0.0),  # Green
    # fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
    # fancy.CRGB(0.0, 0.0, 1.0),  # Blue
    # fancy.CRGB(0.5, 0.0, 0.5),  # Magenta
]

# Declare a NeoPixel object on pin D6 with num_leds pixels, no auto-write.
# Set brightness to max because we'll be using FancyLED's brightness control.
pixels1 = neopixel.NeoPixel(board.GP14, num_leds, brightness=1.0, auto_write=False)
pixels2 = neopixel.NeoPixel(board.GP15, num_leds, brightness=1.0, auto_write=False)

offset = 0  # Positional offset into color palette to get it to 'spin'

while True:
    for i in range(num_leds):
        # Load each pixel's color from the palette using an offset, run it
        # through the gamma function, pack RGB value and assign to pixel.
        color = fancy.palette_lookup(palette, offset + i / num_leds)
        color = fancy.gamma_adjust(color, brightness=0.9)
        pixels1[i] = color.pack()
        pixels2[i] = color.pack()
    pixels1.show()
    pixels2.show()
    offset += 0.001  # Bigger number = faster spin
