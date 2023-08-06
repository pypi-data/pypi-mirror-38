import math


def difference(d1, d2, units='ms'):
    """ calculate the difference between two timestamps (in the given units) """
    multiplier = {
        'ms': 1000,
        's': 1,
        'm': 1 / 60,
        'h': 1 / (60 * 60)
    }

    return math.ceil((d1 - d2).total_seconds() * multiplier[units])