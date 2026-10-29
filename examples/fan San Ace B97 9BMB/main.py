import time
import board
import analogio
import pulseio
import pwmio

print("example: fan San Ace B97 9BMB (9BMB12P2K01)")
# datasheet:
# /home/stefan/mydata/parts_info/San Ace SanyoDenki/San Ace B97 9BMB/9BMB12P2K01 details.md

# analog input (potentiometer) on GP27 / A1 sets the speed
pot = analogio.AnalogIn(board.GP27)

# fan PWM input: 25kHz.
# PWM line is driven through an inverting BC547C NPN stage
# (see san_ace_fan_rp2040_summary.md): GPIO high = fan PWM line low.
PWM_INVERT = True
PWM_FREQUENCY = 25000
# datasheet: operate at 20% duty or above; 0% = stop.
DUTY_MIN = 0.20
# below this pot position the fan is switched off
POT_OFF_THRESHOLD = 0.03

fan_pwm = pwmio.PWMOut(
    board.GP3,
    frequency=PWM_FREQUENCY,
    duty_cycle=65535 if PWM_INVERT else 0,
)

# tacho: open collector, needs the external pull-up to 3V3 (never 5V!).
# countio.Counter does not work here: on the RP2040 it needs a PWM channel B
# pin (odd GPIO) and GP2 is channel A. PulseIn works on any pin.
# the output toggles 4 times per revolution -> every recorded pulse (high or
# low time) is one edge = 1/4 revolution.
tacho = pulseio.PulseIn(board.GP2, maxlen=128, idle_state=True)
TACHO_EDGES_PER_REVOLUTION = 4

POT_SMOOTHING = 0.1
RPM_INTERVAL = 1.0
PRINT_INTERVAL = 0.5

pot_value = pot.value / 65535
duty = 0.0
rpm = 0
tacho_edges = 0
tacho_last_time = time.monotonic()
print_last_time = tacho_last_time


def fan_duty_set(duty_percent):
    """Set fan speed. 0.0 = off, 1.0 = full speed."""
    duty_percent = min(1.0, max(0.0, duty_percent))
    value = int(duty_percent * 65535)
    if PWM_INVERT:
        value = 65535 - value
    fan_pwm.duty_cycle = value


def pot_to_duty(pot_norm):
    """Map pot position 0..1 to duty: off, or DUTY_MIN..1.0."""
    if pot_norm < POT_OFF_THRESHOLD:
        return 0.0
    span = 1.0 - POT_OFF_THRESHOLD
    return DUTY_MIN + (pot_norm - POT_OFF_THRESHOLD) / span * (1.0 - DUTY_MIN)


def rpm_update():
    global rpm, tacho_last_time, tacho_edges
    # drain the buffer every call so it can't overflow (~460 edges/s at full speed)
    tacho_edges += len(tacho)
    tacho.clear()
    now = time.monotonic()
    elapsed = now - tacho_last_time
    if elapsed >= RPM_INTERVAL:
        rpm = int(tacho_edges / TACHO_EDGES_PER_REVOLUTION / elapsed * 60)
        tacho_edges = 0
        tacho_last_time = now


def main():
    global pot_value, duty, print_last_time

    # smooth the analog reading (low pass) to avoid jitter
    pot_value += (pot.value / 65535 - pot_value) * POT_SMOOTHING
    duty = pot_to_duty(pot_value)
    fan_duty_set(duty)

    rpm_update()

    now = time.monotonic()
    if (now - print_last_time) >= PRINT_INTERVAL:
        print_last_time = now
        print(
            "pot: {:5.1f}%  duty: {:5.1f}%  rpm: {:5d}".format(
                pot_value * 100, duty * 100, rpm
            )
        )

    time.sleep(0.01)


while True:
    main()
