# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple FancyLED example for NeoPixel strip"""

import board
import neopixel

import adafruit_fancyled.adafruit_fancyled as fancy

from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle

from adafruit_led_animation.animation.comet import Comet

from adafruit_led_animation.color import PURPLE

from adafruit_led_animation.sequence import AnimationSequence


num_leds = 20
pixels1 = neopixel.NeoPixel(board.GP14, num_leds, brightness=0.5, auto_write=False)
pixels2 = neopixel.NeoPixel(board.GP15, num_leds, brightness=0.5, auto_write=False)

animation1 = RainbowComet(pixels1, speed=0.07, tail_length=7, colorwheel_offset=30)
animation2 = Comet(pixels2, speed=0.02, color=PURPLE, tail_length=10, )

while True:
    animation1.animate()
    animation2.animate()
