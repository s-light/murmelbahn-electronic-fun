# detection logic for one reflective light barrier channel
# (no hardware access, so it can be tested on a PC)

# return values of Channel.update()
NOTHING = 0
TRIGGERED = 1
RELEASED = 2

# consecutive samples needed to change the state
SAMPLES_ON = 2
SAMPLES_OFF = 3

RAW_MAX = 65535


class Channel:
    """adaptive threshold detector with hysteresis.

    the sensor value *drops* if something reflects light, so
    signal = baseline - raw value
    triggered if signal > threshold, released if signal < threshold / 2
    """

    def __init__(self, name, threshold, baseline_alpha=0.005):
        self.name = name
        self.threshold = threshold
        self.baseline_alpha = baseline_alpha
        self.reset(RAW_MAX)

    def reset(self, value):
        """start over with `value` as baseline."""
        self.baseline = value
        self.last = value
        self.triggered = False
        self.was_triggered = False
        self.peak = 0
        self.frame_min = RAW_MAX
        self._count = 0

    def update(self, value):
        """process one sample. called as often as possible."""
        self.last = value
        if value < self.frame_min:
            self.frame_min = value
        signal = self.baseline - value

        if not self.triggered:
            if signal <= self.threshold:
                self._count = 0
                return NOTHING
            self._count += 1
            if self._count < SAMPLES_ON:
                return NOTHING
            self._count = 0
            self.triggered = True
            self.was_triggered = True
            self.peak = signal
            return TRIGGERED

        if signal > self.peak:
            self.peak = signal
        if signal >= self.threshold / 2:
            self._count = 0
            return NOTHING
        self._count += 1
        if self._count < SAMPLES_OFF:
            return NOTHING
        self._count = 0
        self.triggered = False
        return RELEASED

    def end_frame(self):
        """call in a fixed interval.

        lets the baseline follow slow changes and returns
        (lowest value, triggered at any time) of the last interval.
        """
        result = (self.frame_min, self.was_triggered)
        # hold the baseline while something is in front of the sensor
        if not self.triggered and self._count == 0:
            self.baseline += (self.last - self.baseline) * self.baseline_alpha
        self.frame_min = RAW_MAX
        self.was_triggered = self.triggered
        return result
