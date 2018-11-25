
import functools
import math


def calculate_rms(signal):
    return math.sqrt(functools.reduce(lambda x,y: x + y, map(lambda x: x * x, signal)))


def calculate_power_factor(voltage, current):
    voltage_rms = calculate_rms(voltage)
    current_rms = calculate_rms(current)
    apparent_power = voltage_rms * current_rms
    power = functools.reduce(lambda x,y: x + y, [a * b for a,b in zip(voltage, current)])
    return power / apparent_power


def calculate_total_harmonic_distortion(signal):
    return []

