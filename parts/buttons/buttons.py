# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple FancyLED example for NeoPixel strip"""


import time
import board
import keypad


keys = keypad.Keys(
    (
        # onboard buttons
        board.GP20,
        board.GP21,
        # GROVE dual Button on `GROVE 2` port.
        board.GP2,
        board.GP3,
    ),
    value_when_pressed=False,
    pull=True,
)


while True:
    event = keys.events.get()
    # event will be None if nothing has happened.
    if event:
        print(event)
