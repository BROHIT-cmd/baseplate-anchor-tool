import math

from data import *

def calculate_operating_load(weight):

    return weight * 9.81 / 1000


def support_spacing(pipe_size):

    return SUPPORT_SPACING[pipe_size]


def support_quantity(pipe_length, spacing):

    return math.ceil(pipe_length / spacing) + 1


def support_locations(pipe_length, spacing):

    loc = []

    current = 0

    while current < pipe_length:

        loc.append(round(current,2))

        current += spacing

    loc.append(pipe_length)

    return loc


def recommend_anchor(weight):

    if weight <= 1500:
        return "M16"

    elif weight <= 3000:
        return "M20"

    elif weight <= 5000:
        return "M24"

    else:
        return "M30"


def recommend_baseplate(weight):

    if weight <= 1500:

        return 1500,700,12

    elif weight <= 3000:

        return 2000,800,15

    elif weight <= 5000:

        return 2500,900,20

    else:

        return 3000,1000,25
