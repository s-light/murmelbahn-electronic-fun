# light barrier for marbles with two reflective sensor channels
# on Cytron Maker Pi RP2040
#
# wiring (Grove 6):
#   GP27 = sensor A output (analog)
#   GP26 = sensor B output (analog)
#   sensor CTRL not connected -> LEDs run with full current
#
# controls:
#   button GP20 = less sensitive   button GP21 = more sensitive
#   serial (console or data port):
#     + threshold up     - threshold down     <number> + Enter: set threshold
#     c recalibrate      m buzzer on/off      s status        ? help
#
# onboard pixel LEDs: A = green, B = blue
# plot data is send to the second USB serial port (see README.md)

import time

import analogio
import board
import digitalio
import neopixel_write
import pwmio
import supervisor
import usb_cdc

import barrier

PIN_SENSOR_A = board.GP27
PIN_SENSOR_B = board.GP26
PIN_BUTTON_LESS = board.GP20
PIN_BUTTON_MORE = board.GP21
PIN_BUZZER = board.GP22
PIN_PIXELS = board.GP18

# distance between the two sensor spots in travel direction
# 4mm = both channels of one QTR-HD-02A
SENSOR_DISTANCE_MM = 4.0
# both channels have to trigger within this time to count as one marble
PAIR_WINDOW_MS = 200

THRESHOLD_DEFAULT = 2000
THRESHOLD_STEP = 250
THRESHOLD_MIN = 500
THRESHOLD_MAX = 30000

FRAME_MS = 10  # baseline update and plot output
STUCK_MS = 3000  # triggered longer than this -> new baseline
BEEP_MS = 30
# value of the trigger channel in the plot while triggered
PLOT_TRIGGER_VALUE = 5000

_TICKS_MASK = (1 << 29) - 1


def ticks_since(start):
    """milliseconds since `start` (supervisor.ticks_ms wraps around)."""
    return (supervisor.ticks_ms() - start) & _TICKS_MASK


sensors = (analogio.AnalogIn(PIN_SENSOR_A), analogio.AnalogIn(PIN_SENSOR_B))
channels = (
    barrier.Channel("A", THRESHOLD_DEFAULT),
    barrier.Channel("B", THRESHOLD_DEFAULT),
)
trigger_ticks = [0, 0]
trigger_ns = [0, 0]
# a trigger which still waits for the other channel
unpaired = [False, False]


def make_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.switch_to_input(pull=digitalio.Pull.UP)
    return button


buttons = (
    (make_button(PIN_BUTTON_LESS), THRESHOLD_STEP),
    (make_button(PIN_BUTTON_MORE), -THRESHOLD_STEP),
)
# state of the last two frames -> debounce
button_history = [0, 0]

buzzer = pwmio.PWMOut(PIN_BUZZER, frequency=880, variable_frequency=True)
buzzer_enabled = True
beep_start = None

pixel_pin = digitalio.DigitalInOut(PIN_PIXELS)
pixel_pin.switch_to_output()
pixel_buffer = bytearray(6)  # 2 pixels, order G R B


def show_pixels():
    pixel_buffer[0] = 40 if channels[0].triggered else 0
    pixel_buffer[5] = 40 if channels[1].triggered else 0
    neopixel_write.neopixel_write(pixel_pin, pixel_buffer)


def beep(frequency):
    global beep_start
    if buzzer_enabled:
        buzzer.frequency = frequency
        buzzer.duty_cycle = 32768
        beep_start = supervisor.ticks_ms()


def calibrate():
    for sensor, channel in zip(sensors, channels):
        total = 0
        for _ in range(200):
            total += sensor.value
            time.sleep(0.001)
        channel.reset(total // 200)
        print("{}: baseline {}".format(channel.name, int(channel.baseline)))
        if channel.baseline - channel.threshold <= 0:
            print("   something very reflective in front? it can not trigger!")
        elif channel.baseline > 64500:
            print("   no reflection at all - is a sensor connected?")
    unpaired[0] = unpaired[1] = False
    show_pixels()


def set_threshold(value):
    value = min(max(value, THRESHOLD_MIN), THRESHOLD_MAX)
    for channel in channels:
        channel.threshold = value
    print("threshold: on {} / off {}".format(value, value // 2))


def print_help():
    print("commands: + threshold up, - threshold down, <number>+Enter set it")
    print("          c recalibrate, m buzzer on/off, s status, ? help")


def print_status():
    for channel in channels:
        print(
            "{}: raw {}, baseline {}, threshold {}{}".format(
                channel.name,
                channel.last,
                int(channel.baseline),
                channel.threshold,
                ", TRIGGERED" if channel.triggered else "",
            )
        )
    print(
        "loop: {} samples/s per channel, longest frame {}ms".format(
            samples_per_second, longest_frame_ms
        )
    )


def handle_char(char, number):
    """process one received character. returns the collected digits."""
    global buzzer_enabled
    if char.isdigit():
        return (number + char)[-5:]
    if char in "\r\n":
        if number:
            set_threshold(int(number))
    elif char == "+":
        set_threshold(channels[0].threshold + THRESHOLD_STEP)
    elif char == "-":
        set_threshold(channels[0].threshold - THRESHOLD_STEP)
    elif char == "c":
        calibrate()
    elif char == "m":
        buzzer_enabled = not buzzer_enabled
        print("buzzer", "on" if buzzer_enabled else "off")
    elif char == "s":
        print_status()
    elif char == "?":
        print_help()
    return ""


def on_triggered(index):
    trigger_ticks[index] = supervisor.ticks_ms()
    trigger_ns[index] = time.monotonic_ns()
    other = 1 - index
    if unpaired[other] and ticks_since(trigger_ticks[other]) <= PAIR_WINDOW_MS:
        unpaired[other] = False
        delta_ms = (trigger_ns[index] - trigger_ns[other]) / 1000000
        direction = "{} -> {}".format(channels[other].name, channels[index].name)
        if delta_ms > 0.5:
            print(
                "marble {}: {:.1f}ms = {:.2f}m/s".format(
                    direction, delta_ms, SENSOR_DISTANCE_MM / delta_ms
                )
            )
        else:
            print("marble: both channels at once, no direction")
    else:
        unpaired[index] = True
    beep(880 if index == 0 else 1320)
    show_pixels()


def on_released(index):
    channel = channels[index]
    print(
        "{}: {}ms, signal {} (threshold {})".format(
            channel.name,
            ticks_since(trigger_ticks[index]),
            int(channel.peak),
            channel.threshold,
        )
    )
    show_pixels()


plot_port = usb_cdc.data
if plot_port:
    # never block the loop if nobody reads the data
    plot_port.write_timeout = 0
else:
    print("no data port! copy boot.py and press the reset button.")

serial_ports = [port for port in (usb_cdc.console, plot_port) if port]
# collected digits, separate per port
numbers = [""] * len(serial_ports)


def frame():
    """everything which does not need to run at full speed."""
    global beep_start

    values = []
    for index, channel in enumerate(channels):
        lowest, was_triggered = channel.end_frame()
        values.append(
            "{n}:{},{n}_base:{},{n}_thresh:{},{n}_trig:{}".format(
                lowest,
                int(channel.baseline),
                max(int(channel.baseline) - channel.threshold, 0),
                PLOT_TRIGGER_VALUE if was_triggered else 0,
                n=channel.name.lower(),
            )
        )
        if channel.triggered and ticks_since(trigger_ticks[index]) > STUCK_MS:
            print("{}: stuck, new baseline".format(channel.name))
            channel.reset(channel.last)
            show_pixels()

    if plot_port and plot_port.connected:
        plot_port.write((",".join(values) + "\n").encode())

    for index, (button, step) in enumerate(buttons):
        button_history[index] = ((button_history[index] << 1) | (not button.value)) & 7
        # released, then two frames pressed
        if button_history[index] == 0b011:
            set_threshold(channels[0].threshold + step)

    for index, port in enumerate(serial_ports):
        if port.in_waiting:
            for byte in port.read(port.in_waiting):
                numbers[index] = handle_char(chr(byte), numbers[index])

    if beep_start is not None and ticks_since(beep_start) >= BEEP_MS:
        buzzer.duty_cycle = 0
        beep_start = None


samples_per_second = 0
longest_frame_ms = 0

print()
print("marble light barrier")
print_help()
calibrate()
set_threshold(THRESHOLD_DEFAULT)

sensor_a, sensor_b = sensors
channel_a, channel_b = channels
frame_start = statistics_start = supervisor.ticks_ms()
sample_count = 0
longest = 0

while True:
    # hot loop: keep it short and without memory allocations
    event = channel_a.update(sensor_a.value)
    if event:
        if event == barrier.TRIGGERED:
            on_triggered(0)
        else:
            on_released(0)
    event = channel_b.update(sensor_b.value)
    if event:
        if event == barrier.TRIGGERED:
            on_triggered(1)
        else:
            on_released(1)
    sample_count += 1

    elapsed = ticks_since(frame_start)
    if elapsed >= FRAME_MS:
        frame_start = supervisor.ticks_ms()
        longest = max(longest, elapsed)
        frame()
        interval = ticks_since(statistics_start)
        if interval >= 1000:
            samples_per_second = sample_count * 1000 // interval
            longest_frame_ms = longest
            statistics_start = supervisor.ticks_ms()
            sample_count = 0
            longest = 0
