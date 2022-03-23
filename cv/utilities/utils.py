
r"""
Environment utilities.

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("utilities/utils.py", ""))
from typing import Dict

import numpy as np
import cv2

from utilities.env import get_args


def get_configs(path2config) -> Dict:
    args = get_args()


def read_image(path2image: os.PathLike) -> np.ndarray:
    image = cv2.imread(path2image, -1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).transpose(2, 0, 1)
    return image
