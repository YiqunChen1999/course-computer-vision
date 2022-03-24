
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
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).transpose(2, 0, 1)
    return image


def save_image(path2image: os.PathLike, image: np.ndarray):
    if len(image.shape) == 3 and image.shape[0] == 3:
        image.transpose(1, 2, 0)
    return cv2.imwrite(path2image, image)


def argtopk(arr: np.ndarray, k: int, axis: int=-1) -> np.ndarray:
    r"""Return the indices of topk elements."""
    return np.argsort(arr, axis=axis)[-k:]


def topk(arr: np.ndarray, k: int, axis: int=-1) -> np.ndarray:
    return arr[argtopk(arr, k, axis)]


