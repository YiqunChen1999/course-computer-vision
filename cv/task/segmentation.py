
r"""
Histogram calculator.

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("task/segmentation.py", ""))

import numpy as np
import cv2
import skimage
from skimage import exposure

from utilities.configs import Configs
from utilities.utils import read_image


def segment_by_histogram(image: np.ndarray) -> np.ndarray:
    hist = exposure.histogram(image)
    

def segment(path2image: os.PathLike, configs: Configs) -> np.ndarray:
    image = read_image(path2image)
    raise NotImplementedError("NotImplementedError")


def segment_multiple_images(directory: os.PathLike, configs: Configs):
    files = os.listdir(directory)
    valid_type = ["png", "jpg", "jpeg"]

    # Filter invalid files.
    files = list(filter(lambda x: x.split(".")[-1] in valid_type), files)
    for fn in files:
        path2image = os.path.join(directory, fn)
        result = segment(path2image, configs)
