from dataclasses import dataclass
from typing import Optional
from vl8.dsp import curve_cache
from vl8.function.periodic import Periodic
from vl8.types import to_number, types
import math
import numpy as np


@dataclass
class Waveform(Periodic):
    curve: curve_cache.Curve = None
    duty_cycle: Optional[types.Number] = None

    @property
    def nperiods(self):
        return self.actual_duration / self.period

    def __call__(self):
        arr = self._create()
        if self._duty_cycle and self._duty_cycle != 0.5:
            _apply_duty_cycle(arr, float(self._duty_cycle))

        self._apply(arr)
        return np.row_stack([arr] * self.nchannels)

    def _apply(self, arr):
        pass

    def _create(self):
        begin = self.phase
        end = begin + self.nperiods
        steps = math.ceil(self.sample_duration)
        arr = np.linspace(2 * begin, 2 * end, steps, dtype=self.dtype)
        arr %= 2
        arr -= 1
        return arr

    def _get_duty_cycle(self):
        return self._duty_cycle

    def _set_duty_cycle(self, dc):
        if dc is not None:
            dc = to_number(dc)
            if not (0 < dc < 1):
                raise ValueError('duty_cycle must be between 0 and 1')
        self._duty_cycle = dc


Waveform.duty_cycle = property(
    Waveform._get_duty_cycle, Waveform._set_duty_cycle
)


class Sawtooth(Waveform):
    def _apply(self, arr):
        pass


class Sine(Waveform):
    def _apply(self, arr):
        arr *= np.pi
        np.sin(arr, out=arr)


class Square(Waveform):
    def _apply(self, arr):
        arr[arr < 0] = -1
        arr[arr >= 0] = 1


class Triangle(Waveform):
    def _apply(self, arr):
        below = arr < 0
        above = arr >= 0

        arr[below] *= 2
        arr[below] += 1

        arr[above] *= -2
        arr[above] += 1


def _apply_duty_cycle(arr, dc):
    # This appears to do nothing.
    below = arr < dc
    above = arr >= dc

    arr[below] *= 1 / dc
    arr[below] -= 1

    arr[above] -= dc
    arr[above] *= 1 / (1 - dc)
