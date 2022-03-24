
r"""
Histogram calculator.

author: 
    Yiqun Chen
"""

import os
import sys
from typing import Callable, Dict, Union
sys.path.append(__file__.replace("task/segmentation.py", ""))

import numpy as np

from utilities.configs import Configs
from utilities import utils
from utilities.utils import read_image, save_image


SEGMENTATIONS = {}
def register(callable: Callable) -> Callable:
    SEGMENTATIONS[callable.__name__] = callable
    return callable


@register
def segment_by_threshold(configs: Configs, image: np.ndarray) -> np.ndarray:
    r"""Segment an image by threshold."""
    histogram, bin_edges = np.histogram(
        image, bins=configs.segmentation.threshold.bins, range=(0., 255.)
    )
    assert len(histogram.shape) == 1, histogram.shape
    thre = configs.segmentation.threshold.thre
    if thre == "auto":
        argtopk = utils.argtopk(histogram, 2)
        thre = np.mean([
            bin_edges[argtopk[0]], bin_edges[argtopk[0]+1], 
            bin_edges[argtopk[1]], bin_edges[argtopk[1]+1], 
        ])
    # TODO TODO Do something to segment the image.
    lower_idx = image <= thre
    upper_idx = image > thre
    segmap = np.zeros_like(image, dtype=np.int16)
    segmap[upper_idx] = 255
    return segmap


def segment_one_image(configs: Configs, path2image: os.PathLike) -> np.ndarray:
    r"""Segment one image by method specified in configs."""
    image = read_image(path2image)
    method = f"segment_by_{configs.segmentation.method}"
    segfunc = SEGMENTATIONS[method]
    return segfunc(configs, image)


def segment_multiple_images(configs: Configs):
    r"""
    Segment all images in one directory and save to 
    the directory specified in configs.
    """
    image_root = configs.image.root
    result_root = configs.result.root
    files = os.listdir(image_root)
    valid_type: list = configs.image.filetype

    # Filter invalid files.
    files = list(filter(
        lambda x: x.split(".")[-1].lower() in valid_type, files
    ))
    for fn in files:
        path2image = os.path.join(image_root, fn)
        result = segment_one_image(configs, path2image)
        path2segmap = os.path.join(result_root, fn)
        success = save_image(path2segmap, result)
        if success:
            print(f"Save segmentation map to {path2segmap}.")
        else:
            print(f"Failed to save segmentation map to {path2segmap}.")


