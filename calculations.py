from anchor_data import *

def calculate_pump_load(weight):
    return weight * 9.81 / 1000


def estimate_additional_load(
        pump_load,
        duty_flow,
        head,
        pipe_size,
        pipe_length):

    pipe_factor = (pipe_size * pipe_length) / 100000

    flow_factor = duty_flow / 100

    head_factor = head / 100

    additional_load = (
        pump_load *
        (pipe_factor + flow_factor + head_factor)
    ) * 0.15

    return additional_load


def total_load(pump_load, additional_load):
    return pump_load + additional_load


def load_per_anchor(total_load, anchors):
    return total_load / anchors


def calculate_utilization(load_per_anchor_value, anchor):
    capacity = ANCHOR_CAPACITY[anchor]

    return (
        load_per_anchor_value /
        capacity
    ) * 100


def embedment_depth(anchor, concrete):
    dia = ANCHOR_DIAMETER[anchor]

    factor = CONCRETE_FACTOR[concrete]

    return dia * 10 * factor


def slot_size(anchor):

    hole = HOLE_SIZE[anchor]

    slot_width = hole

    slot_length = hole + 20

    return slot_width, slot_length
