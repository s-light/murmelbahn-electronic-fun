# QTR-HD-02A raw value test on Cytron Maker Pi RP2040
#
# wiring (Grove 6):
#   GP27 = sensor output (analog)
#   GP26 = sensor CTRL (emitter on/off + dimming)
#
# LED intensity:
#   button GP20 = darker      button GP21 = brighter
#   serial (console or data port):
#     +  brighter     -  darker      x  LEDs off     o  LEDs on
#     r  resync       ?  help        0..31 + Enter = set dim level
#
# plot data is send to the second USB serial port in Arduino label format:
#   raw:12345,level:0

import time

import analogio
import board
import digitalio
import usb_cdc

PIN_SENSOR = board.GP27
PIN_CTRL = board.GP26
PIN_BUTTON_DARKER = board.GP20
PIN_BUTTON_BRIGHTER = board.GP21

SAMPLE_INTERVAL = 0.01  # seconds -> 100 Hz
CONSOLE_INTERVAL = 0.5
DEBOUNCE_TIME = 0.02

LEVEL_COUNT = 32  # 0 = full current ... 31 = lowest current


def level_to_percent(level):
    """LED current in percent. the last three steps are only half as big."""
    if level <= 28:
        return 100 - level * 10 / 3
    return 100 - 28 * 10 / 3 - (level - 28) * 5 / 3


class Emitter:
    """CTRL pin of second generation Pololu QTR sensors.

    low >= 1ms: LEDs off, dim level is reset
    low pulse 0.5..300us: next dim level (wraps from 31 to 0)
    """

    def __init__(self, pin):
        self.ctrl = digitalio.DigitalInOut(pin)
        self.ctrl.switch_to_output(value=False)
        self.level = 0
        self.enabled = True
        self.resync()

    def _pulse(self, count):
        ctrl = self.ctrl
        for _ in range(count):
            ctrl.value = False
            ctrl.value = True

    def resync(self):
        """switch off and on again so the sensor is in a known state."""
        self.ctrl.value = False
        time.sleep(0.002)
        if self.enabled:
            self.ctrl.value = True
            time.sleep(0.001)
            self._pulse(self.level)

    def set_level(self, level):
        level = min(max(level, 0), LEVEL_COUNT - 1)
        if self.enabled:
            # only forward pulses: no off-glitch between two levels
            self._pulse((level - self.level) % LEVEL_COUNT)
        self.level = level

    def set_enabled(self, enabled):
        if enabled != self.enabled:
            self.enabled = enabled
            self.resync()


class Button:
    """debounced button to GND."""

    def __init__(self, pin):
        self.io = digitalio.DigitalInOut(pin)
        self.io.switch_to_input(pull=digitalio.Pull.UP)
        self.pressed = False
        self.changed_at = 0

    def was_pressed(self, now):
        pressed = not self.io.value
        if pressed == self.pressed or now - self.changed_at < DEBOUNCE_TIME:
            return False
        self.pressed = pressed
        self.changed_at = now
        return pressed


def print_state():
    if emitter.enabled:
        print(
            "LEDs on, level {} = {:.1f}% current".format(
                emitter.level, level_to_percent(emitter.level)
            )
        )
    else:
        print("LEDs off (level {} stored)".format(emitter.level))


def print_help():
    print("commands: + brighter, - darker, x off, o on, r resync, ? help")
    print("          0..31 + Enter: set dim level (0 = brightest)")


def handle_char(char, number):
    """process one received character. returns the collected digits."""
    if char.isdigit():
        return (number + char)[-2:]
    if char in "\r\n":
        if not number:
            return ""
        emitter.set_level(int(number))
    elif char == "+":
        emitter.set_level(emitter.level - 1)
    elif char == "-":
        emitter.set_level(emitter.level + 1)
    elif char == "x":
        emitter.set_enabled(False)
    elif char == "o":
        emitter.set_enabled(True)
    elif char == "r":
        emitter.resync()
    elif char == "?":
        print_help()
    else:
        return ""
    print_state()
    return ""


sensor = analogio.AnalogIn(PIN_SENSOR)
emitter = Emitter(PIN_CTRL)
button_darker = Button(PIN_BUTTON_DARKER)
button_brighter = Button(PIN_BUTTON_BRIGHTER)

plot_port = usb_cdc.data
if plot_port:
    # never block the loop if nobody reads the data
    plot_port.write_timeout = 0
else:
    print("no data port! copy boot.py and press the reset button.")

serial_ports = [port for port in (usb_cdc.console, plot_port) if port]
# collected digits, separate per port
numbers = [""] * len(serial_ports)

print()
print("QTR-HD-02A raw value test")
print_help()
print_state()

next_sample = time.monotonic()
next_console = next_sample

while True:
    now = time.monotonic()

    if button_darker.was_pressed(now):
        emitter.set_level(emitter.level + 1)
        print_state()
    if button_brighter.was_pressed(now):
        emitter.set_level(emitter.level - 1)
        print_state()

    for index, port in enumerate(serial_ports):
        if port.in_waiting:
            for byte in port.read(port.in_waiting):
                numbers[index] = handle_char(chr(byte), numbers[index])

    if now >= next_sample:
        next_sample += SAMPLE_INTERVAL
        if next_sample < now:
            next_sample = now + SAMPLE_INTERVAL
        # 0..65535 (12bit ADC scaled to 16bit)
        # bright / high reflectance = low value
        raw = sensor.value
        line = "raw:{},level:{}".format(raw, emitter.level)

        if plot_port and plot_port.connected:
            plot_port.write((line + "\n").encode())

        if now >= next_console:
            next_console = now + CONSOLE_INTERVAL
            print(line if emitter.enabled else line + " (LEDs off)")
