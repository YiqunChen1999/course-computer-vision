
r"""
Define some colors.
"""

from typing import Tuple

import numpy as np


COLORS = (
    (  0,   0, 255), 
    (  0, 255,   0), 
    (255,   0,   0), 

    (255,   0, 255), 
    (255, 255,   0), 
    (  0,   0, 255), 

    (  0,   0,   0), 
    (255, 255, 255), 
    (128, 128, 128), 

    (  0,   0, 128), 
    (  0, 128,   0), 
    (128,   0,   0), 
    
    (128,   0, 128), 
    (128, 128,   0), 
    (  0,   0, 128), 

    (240, 135, 132), 
    (119,  67,  66), 
    (115, 251, 253), 
)


def get_colors(num: int) -> Tuple[Tuple[int, int, int]]:
    if num <= len(COLORS):
        return COLORS[: num]
    return COLORS + generate_colors(num - len(COLORS))


def generate_colors(num: int) -> Tuple[Tuple[int, int, int]]:
    valid_number = (0, 64, 128, 192, 255)
    generated = []
    while len(generated) < num:
        color = tuple(np.random.choice(valid_number, 3, False))
        if color in ((0, 0, 0), ) + COLORS + tuple(generated):
            continue
        generated.append(color)
    return tuple(generated)

