# QTR-HD-02A raw value test

prints the raw ADC value of one channel of a
[Pololu QTR-HD-02A](https://www.pololu.com/product/4202) reflectance sensor
and lets you change the LED intensity.

Controller: Cytron Maker Pi RP2040 with CircuitPython (tested with 10.3.2).
No additional libraries needed.

## wiring

| sensor | Maker Pi RP2040 (Grove 6) |
| ------ | ------------------------- |
| OUT    | GP27                      |
| CTRL   | GP26                      |
| VCC    | 3V3                       |
| GND    | GND                       |

## install

copy `boot.py` and `code.py` to the `CIRCUITPY` drive, then press the reset button
(`boot.py` is only read after a reset).

## serial ports

| port           | usual name     | content                           |
| -------------- | -------------- | --------------------------------- |
| console (if00) | `/dev/ttyACM0` | REPL, state messages, values 2 Hz |
| data (if02)    | `/dev/ttyACM1` | plot data only, 100 Hz            |

data format (*Arduino Serial Labels*): `raw:12345,level:0`

- `raw`: 0..65535 - higher reflectance gives a **lower** value
- `level`: dim level 0 (100% LED current) .. 31 (1.67%)

## LED intensity

- button GP20: darker, button GP21: brighter
- send to console or data port:
  `+` brighter, `-` darker, `x` off, `o` on, `r` resync, `?` help,
  `0`..`31` followed by Enter to set the level

Protocol of the CTRL pin:
[Pololu documentation](https://www.pololu.com/docs/0J13/4)

## plot

in [SerialPlot](https://github.com/hyOzd/serialplot): *File → Load Settings* →
`serialplot.ini`, then open the port.
The `level` channel is shown with gain 1000 so it is visible next to `raw`.
