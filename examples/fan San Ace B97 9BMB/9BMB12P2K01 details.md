# San Ace B97 – 9BMB12P2K01 (12 V PWM variable speed fan)

Source: `9BMB12P2K01 details.pdf` (SANYO DENKI CO., LTD., drawing no. 9BMB12P2K01 rev. D, pages 1/2 and 2/2; sensor spec 9D0001H111 rev. B).

## Specification (page 1)

| Item                                  | Value                                   |
| ------------------------------------- | --------------------------------------- |
| PWM duty cycle (for the values below) | 100 %                                   |
| Rated voltage                         | 12 V DC                                 |
| Operating voltage                     | 10.8 V DC ~ 13.2 V DC                   |
| Rated current                         | 3.4 A at 12 V DC                        |
| Rated speed                           | 6850 ± 680 min⁻¹ at 12 V DC (at 25 °C)  |
| Insulation resistance                 | 10 MΩ min. at 500 V DC (note 2)         |
| Dielectric strength                   | 1 minute at 500 V AC, 50/60 Hz (note 2) |
| Operating temperature                 | −20 °C ~ +70 °C                         |
| Sound pressure level                  | 66 dB(A) nominal (note 1)               |
| Mass                                  | approx. 190 g                           |
| Material                              | frame, impeller: plastics               |
| Bearing system                        | 2 ball bearings                         |

### Control terminal

| Item                     | Value                               |
| ------------------------ | ----------------------------------- |
| Source current           | 1 mA max. at control voltage 0 V    |
| Sink current             | 1 mA max. at control voltage 5.25 V |
| Control terminal voltage | 5.25 V max. (open circuit)          |

### Lead wires (UL1430 AWG24, 300 ± 30 mm)

| Colour | Function                       |
| ------ | ------------------------------ |
| Red    | + (supply)                     |
| Black  | − (GND)                        |
| Yellow | SENSOR (tacho, open collector) |
| Brown  | CONTROL (PWM input)            |

### Dimensions (approx., mm)

Blower, 97.1 ± 1 × 95 ± 1 (outline), thickness 33 ± 1, impeller ⌀56 ± 1, 4 × ⌀4.5 ± 0.3 mounting holes.
See the PDF for the full drawing.

### Notes (page 1)

1. Sound level measured at 1 m distance from the air inlet.
2. Measured between the lead wires and the frame.
3. The motor is protected against damage from a locked rotor condition at the operating voltage.
4. A label shows product name, model no., manufacturer and manufacturing date.
5. All values are at room temperature and normal humidity.
6. For the sensor spec see 9D0001H111. PWM switching may influence the sensor output.

### Performance curve (100 % duty)

Static pressure vs. air flow (read from the chart, approximate):

| Air flow (m³/min) | Static pressure (Pa) |
| ----------------- | -------------------- |
| 0                 | ~1270 (max.)         |
| 0.5               | ~1100                |
| 1.0               | ~720                 |
| 1.5               | ~100                 |
| ~1.6              | 0 (max. air flow)    |

## PWM control (page 2)

### Input signal

- Duty cycle (%) = T1 / T × 100 (T1 = high time, T = period).
- **PWM frequency: 25 kHz.**
- V_IH = 4.75 V ~ 5.25 V, V_IL = 0 V ~ 0.4 V.
- Rise / fall time (10 % ↔ 90 %): 1 µs max.
- Input may be a TTL signal **or** open collector / open drain.
  For open collector / drain input the duty must be given as (T − T2) / T × 100, i.e. the duty is measured on the *inverted* level.
- Internal circuit: control terminal (CTL) has an internal pull-up and a transistor to GND; the PWM source must be able to source/sink about 1 mA.

### Speed vs. duty (12 V DC, 25 kHz, nominal curve)

| Duty (%) | Speed (min⁻¹), approx. |
| -------- | ---------------------- |
| ~8       | 0 (start of the curve) |
| 10       | ~1000                  |
| 20       | ~2200                  |
| 30       | ~3300                  |
| 40       | ~4200                  |
| 50       | ~4900                  |
| 70       | ~5800                  |
| 100      | 6850                   |

### Notes (page 2)

1. At 100 % duty, see page 1 for the speed.
2. **Operate the fan at 20 % duty or above** (start-up).
3. At 0 % duty the speed is 0 min⁻¹.
4. To control the speed to 0 min⁻¹, input 0 % duty.
5. **If the control lead is not connected, the fan runs at the 100 % duty speed.**
6. PWM frequency is 25 kHz.
7. Control by TTL input, or by open collector / open drain input (see duty formula above).

## Sensor (tacho) specification (page 3, 9D0001H111)

- Output circuit: **open collector**.
- V_CE = 13.8 V DC max., I_C = 5 mA max. (V_CE(sat) = 0.6 V max.).
- Pull-up voltage: 13.8 V DC max., external pull-up resistor required.
- Running: the output toggles four times per rotation, T1 ≈ T2 ≈ T3 ≈ T4 ≈ T0 / 4 = 60 / (4 N) s, where N = fan speed in min⁻¹ and T0 = one rotation.
  → **2 full pulses per revolution**, RPM = pulses per second × 30.
  At 6850 min⁻¹ this is about 228 Hz.
- Locked rotor: output is fixed either high (V_OH) or low (0 V).
- PWM switching may influence the sensor output.
