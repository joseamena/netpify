
import math

SAMPLE_RATE = 50000


def capture(sample_count):
    v1 = [math.sin(2 * math.pi * 60 * n / SAMPLE_RATE) for n in range(50000)]
    v2 = [math.sin((2 * math.pi * 60 * n / SAMPLE_RATE) + (2 * math.pi / 3)) for n in range(50000)]
    v3 = [math.sin((2 * math.pi * 60 * n / SAMPLE_RATE) - (2 * math.pi / 3)) for n in range(50000)]
    data = {
        "phases": {
            "V1": v1[:sample_count - 1],
            "V2": v2[:sample_count - 1],
            "V3": v3[:sample_count - 1],
            "I1": [0] * sample_count,
            "I2": [0] * sample_count,
            "I3": [0] * sample_count,
        }
    }
    return data