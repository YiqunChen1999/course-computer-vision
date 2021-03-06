
r"""
Environment utilities.

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("utilities/utils.py", ""))
from typing import Any, Callable, Dict, Iterable

import numpy as np
# import cv2
from PIL import Image, ImageOps

from cv.utilities.env import get_args, loginfo, logstatus


def get_configs(path2config) -> Dict:
    args = get_args()


def get_max_workers() -> int:
    return os.cpu_count() * 4


def read_image(path2image: os.PathLike) -> np.ndarray:
    # image = cv2.imread(path2image, -1)
    image = Image.open(path2image)
    image = ImageOps.exif_transpose(image)
    # image = image.resize((200, 150))
    image = np.asarray(image)
    loginfo(f"Read an image with resolution: {image.shape}")
    return image


def save_image(path2image: os.PathLike, image: np.ndarray):
    if len(image.shape) == 3 and image.shape[2] == 3:
        image.transpose(2, 0, 1)
    image = Image.fromarray(image)
    image.save(path2image, "png")
    return True


def argtopk(arr: np.ndarray, k: int, axis: int=-1) -> np.ndarray:
    r"""Return the indices of topk elements."""
    return np.argsort(arr, axis=axis)[-k:]


def topk(arr: np.ndarray, k: int, axis: int=-1) -> np.ndarray:
    return arr[argtopk(arr, k, axis)]


def standarize_image(image: np.ndarray) -> np.ndarray:
    r"""Standarize image, including image shape, format, etc."""
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = image.transpose(2, 0, 1)
    return image


def filter_invalid_images(
    files: list[str], valid_types: list[str]
) -> list[str]:
    return list(filter(
        lambda x: x.split(".")[-1].lower() in valid_types, files
    ))


