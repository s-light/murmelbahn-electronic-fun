# light barrier

detects a rolling marble (wooden, 30mm) with two reflective sensor channels,
for example both channels of one
[Pololu QTR-HD-02A](https://www.pololu.com/product/4202).
if both channels trigger, direction and speed are calculated.

Controller: Cytron Maker Pi RP2040 with CircuitPython.
No additional libraries needed.

## wiring

| sensor | Maker Pi RP2040 (Grove 6) |
| ------ | ------------------------- |
| OUT A  | GP27                      |
| OUT B  | GP26                      |
| CTRL   | **not connected** (LEDs run with full current) |
| VCC    | 3V3                       |
| GND    | GND                       |

⚠️ do not run [`qtr-hd-02a-raw`](../qtr-hd-02a-raw) with this wiring:
it drives GP26 as output.

## install

copy `boot.py`, `barrier.py` and `code.py` to the `CIRCUITPY` drive.
press the reset button if the second serial port is not there yet.

set `SENSOR_DISTANCE_MM` in `code.py` to the distance of your two sensor spots
(default 4mm = one QTR-HD-02A with both channels in travel direction).

## how it works

- a marble reflects more light, so the sensor value **drops**.
- signal = baseline - raw value. the baseline slowly follows the ambient
  (time constant about 2s) and is hold while triggered.
- triggered: signal > threshold (2 samples).
  released: signal < threshold / 2 (3 samples).
- triggered for more than 3s: the current value is the new baseline.

## controls

- button GP20: less sensitive, button GP21: more sensitive
- send to console or data port:
  `+` / `-` threshold up / down, `<number>` + Enter set threshold,
  `c` recalibrate (keep the view free), `m` buzzer on/off,
  `s` status (values, samples per second), `?` help
- buzzer and onboard pixel LEDs show a trigger (A = green, B = blue)

## console output

```
marble A -> B: 4.2ms = 0.95m/s
A: 21ms, signal 7350 (threshold 2000)
```

`signal` is the biggest difference to the baseline during this trigger.
for a reliable setup it should be well above the threshold.

## plot

second serial port (usually `/dev/ttyACM1`), every 10ms:

```
a:..,a_base:..,a_thresh:..,a_trig:..,b:..,b_base:..,b_thresh:..,b_trig:..
```

- `a`: lowest raw value in this interval, so short events stay visible
- `a_base`: baseline
- `a_thresh`: the raw value has to go below this line to trigger
- `a_trig`: 5000 while triggered, otherwise 0

```bash
serialplot -c serialplot.ini -p ttyACM1 -o
```

## background

best is no background at all (several cm free space behind the marble).
black for the eye is not necessarily black for infrared: compare materials with
the raw value - the higher the value, the darker.
