# # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# # SPDX-License-Identifier: MIT

# """Simple FancyLED example for NeoPixel strip"""

# import board
# import neopixel

# import adafruit_fancyled.adafruit_fancyled as fancy

# palette = [
#     fancy.CRGB(1.0, 0.0, 0.0),  # Red
#     fancy.CRGB(0.5, 0.5, 0.0),  # Yellow
#     fancy.CRGB(0.0, 1.0, 0.0),  # Green
#     fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
#     fancy.CRGB(0.0, 0.0, 1.0),  # Blue
#     fancy.CRGB(0.5, 0.0, 0.5),  # Magenta
# ]

# # Declare a NeoPixel object on pin D6 with num_leds pixels, no auto-write.
# # Set brightness to max because we'll be using FancyLED's brightness control.
# pixels1 = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1.0, auto_write=False)
# pixels1 = neopixel.NeoPixel(board.IO, 1, brightness=1.0, auto_write=False)

# offset = 0  # Positional offset into color palette to get it to 'spin'

# while True:
#     # Load each pixel's color from the palette using an offset, run it
#     # through the gamma function, pack RGB value and assign to pixel.
#     color = fancy.palette_lookup(palette, offset)
#     color = fancy.gamma_adjust(color, brightness=0.9)
#     pixels1[0] = color.pack()
#     pixels1.show()
#     offset += 0.001  # Bigger number = faster spin
#     time.sleep(0.01)

import board
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixels[0] = (10, 0, 0)