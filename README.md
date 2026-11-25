# murmelbahn electronic fun
collection of examples for marble-runs with electronic things..

![./media/20250831_144952-cut-640x360.av](media/20250831_144952-cut-640x360-30.avif)


## Material (HW)

- controller [CYTRON MAKER PI RP2040](https://github.com/CytronTechnologies/MAKER-PI-RP2040) ([digikey.de](https://www.digikey.de/en/products/detail/cytron-technologies-sdn-bhd/MAKER-PI-RP2040/14557836))
- Pixel-LED-Strip: [BTF-LIGHTING WS2812B ECO 60LEDs/m](https://www.btf-lighting.com/en-intl/products/ws2812b-eco-led-pixel-strip?variant=46553813647586) [(amazon.de)](https://www.amazon.de/dp/B088BDLMH2)
- Button: [Grove - Dual Button](https://www.seeedstudio.com/Grove-Dual-Button-p-4529.html) [(digikey.de)](https://www.digikey.de/en/products/detail/seeed-technology-co-ltd/111020103/12086987)
- Grove cable extender: [M5Stack Grove to Grove Connector](https://shop.m5stack.com/products/connector-grove-to-grove-pin-servo) ([tinytronics.nl](https://www.tinytronics.nl/en/cables-and-connectors/connectors/grove-compatible/m5stack-grove-to-grove-connector-5-pieces))
- Grove cable: `Grove Female Compatible Cable 0.08mm2 - 4p - 100cm` ([tinytronics.nl](https://www.tinytronics.nl/en/cables-and-connectors/cables-and-adapters/grove-compatible/grove-female-compatible-cable-4p-100cm))
- Grove connector: `Grove - universeller 4-poliger Stecker` ([botland.de](https://botland.de/grove-verbindungskabel/13343-grove-universeller-4-poliger-stecker-5904422341664.html))
- Servo extension cable: `Verlängerungskabel für Servos 60cm` ([botland.de](https://botland.de/kabel-fur-servos/648-verlangerungskabel-fur-servos-60cm-5904422329549.html))
- Servo: `MG90S Mini Servo (metal gears)` ([tinytronics.nl](https://www.tinytronics.nl/en/mechanics-and-actuators/motors/servomotors/mg90s-mini-servoc))
- Sensor: `TCS34725 Color Sensor` ([tinytronics.nl](https://www.tinytronics.nl/en/sensors/optical/light-and-color/tcs34725-color-recognition-sensor-module))

- Sensor: [Pololu QTR-HD-02A reflectance sensor](https://www.pololu.com/product/4202)

## structure

| folder | content |
| ------ | ------- |
| [`parts/buttons`](parts/buttons) | onboard and Grove buttons |
| [`parts/fan-san-ace-b97`](parts/fan-san-ace-b97) | PWM fan with speed control and tacho |
| [`parts/led-effects`](parts/led-effects) | pixel LED animations |
| [`parts/lift`](parts/lift) | marble lift |
| [`parts/light-barrier`](parts/light-barrier) | detect a rolling marble, direction and speed |
| [`parts/marble-dispenser`](parts/marble-dispenser) | marble dispenser (CAD) |
| [`parts/marble-reaction`](parts/marble-reaction) | react on a marble: color sensor, gate servo, LEDs |
| [`parts/qtr-hd-02a-raw`](parts/qtr-hd-02a-raw) | reflectance sensor raw values |
| [`parts/servo`](parts/servo) | servo basics |
| [`parts/tcs34725-color`](parts/tcs34725-color) | color sensor |
| [`parts/track-switch`](parts/track-switch) | servo driven track switch |
| [`workshop`](workshop) | complete programs of workshop boards |
| [`common`](common) | shared `boot.py`, libraries and firmware |

## install

copy the script of a part to the `CIRCUITPY` drive and name it `code.py`
(if there is a `code.py` on the drive, a `main.py` is ignored).

- libraries: copy what you need from `common/lib` to `lib` on the drive.
  some scripts also need `adafruit_motor` and `neopixel`, these are not part of this repo -
  get them with [`circup`](https://github.com/adafruit/circup) or the
  [library bundle](https://circuitpython.org/libraries).
- scripts using the second serial port (`usb_cdc.data`) need `common/boot.py`
  (reset the board after copying).

## firmware / software / libraries

[CircuitPython firmware file in this repo](common/firmware)

[Circuitpython for controller `cytron maker pi RP2040`](https://circuitpython.org/board/cytron_maker_pi_rp2040/)

[cytron cp examples for `maker pi RP2040`](https://github.com/CytronTechnologies/MAKER-PI-RP2040/tree/main/Examples/CircuitPython)

[simple led animations](https://learn.adafruit.com/circuitpython-led-animations/basic-animations)

## origin
this project and *Workshop*-Material was first collected for the [`Make Your School MakerFestival 2025`](https://www.makeyourschool.de/maker-festival/)