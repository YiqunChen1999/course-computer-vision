
r"""
Histogram calculator.

author: 
    Yiqun Chen
"""

import math
import os
import sys
sys.path.append(__file__.replace("task/segmentation.py", ""))
import time

import numpy as np

from cv.utilities.configs import Configs
import cv.utilities.utils as utils
from cv.ops.meanshift import MeanShift
from cv.ops.kernel import Gaussian

SEGMENTATIONS = {}
def register(callable):
    SEGMENTATIONS[callable.__name__] = callable
    return callable


@register
def segment_by_threshold(configs: Configs, image: np.ndarray) -> np.ndarray:
    r"""Segment an image by threshold."""
    image = utils.standarize_image(image)
    H, W = image.shape[-2: ]
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
    if len(image.shape) == 3:
        upper_idx = (image[0] > thre) & (image[1] > thre) & (image[2] > thre)
    segmap = np.zeros((H, W), dtype=np.uint8)
    segmap[upper_idx] = 255
    return segmap


@register
def segment_by_local_threshold(
    configs: Configs, image: np.ndarray
) -> np.ndarray:
    r"""Segment an image by local threshold."""
    image = utils.standarize_image(image)
    H, W = image.shape[-2: ]
    patches = configs.segmentation.threshold.patches
    stride_height = math.ceil(H / patches[0])
    stride_width = math.ceil(W / patches[1])
    segmap = np.zeros((H, W), dtype=np.uint8)

    # Split image into patches.
    for row_idx in range(patches[0]):
        for col_idx in range(patches[1]):
            row_start = row_idx * stride_height
            row_end = (row_idx + 1) * stride_height
            col_start = col_idx * stride_width
            col_end = (col_idx + 1) * stride_width
            segmap[row_start: row_end, col_start: col_end] = \
                segment_by_threshold(
                    configs, 
                    image[..., row_start: row_end, col_start: col_end], 
                )

    return segmap

@register
def segment_by_meanshift(
    configs: Configs, image: np.ndarray
) -> np.ndarray:
    solver = MeanShift(
        kernel=Gaussian(), 
        bandwidth=configs.segmentation.meanshift.bandwidth, 
        bins=configs.segmentation.meanshift.bins, 
        tolerance=configs.segmentation.meanshift.tolerance, 
        max_iters=configs.segmentation.meanshift.max_iters, 
    )
    image = utils.standarize_image(image)
    H, W = image.shape[-2: ]
    points = image.copy().reshape(-1, H*W).transpose(1, 0)
    solver.fit(points)
    labels = solver(points)
    labels = labels.reshape(H, W)
    # Assign colors for each cluster.
    if len(image.shape) == 3:
        segmap = np.zeros((H, W, 3), dtype=np.uint8)
    else:
        segmap = np.zeros((H, W), dtype=np.uint8)
    for l in np.unique(labels):
        segmap[labels==l, ...] = solver.centers[l].astype(np.uint8)
    return segmap


def segment_one_image(configs: Configs, path2image: os.PathLike) -> np.ndarray:
    r"""Segment one image by method specified in configs."""
    image = utils.read_image(path2image)
    if configs.segmentation.method == "meanshift":
        print(
            "**NOTE** MeanShift segmentation result may be different between "
            "different runs as MeanShift randomly initialize the "
            "initial cluster centers. The color of cluster centers "
            "will be assigned to each (pixel) cluster."
        )
    method = f"segment_by_{configs.segmentation.method}"
    segfunc = SEGMENTATIONS[method]
    return segfunc(configs, image)


def segment_multiple_images_one_directory(
    configs: Configs, image_root: os.PathLike
):
    r"""
    Segment all images in one directory and save to 
    the directory specified in configs.
    """
    result_root = configs.result.root
    files = os.listdir(image_root)
    valid_type: list = configs.image.filetype

    # Filter invalid files.
    files = list(filter(
        lambda x: x.split(".")[-1].lower() in valid_type, files
    ))
    files = list(filter(
        lambda x: not x.startswith("result_"), files
    ))
    if len(files) == 0:
        print(f"Find no images in folder {image_root}.")
    for fn in files:
        path2image = os.path.join(image_root, fn)
        print(f"Please wait while segmenting image from {path2image}.")
        start = time.time()
        result = segment_one_image(configs, path2image)
        method = configs.segmentation.method
        fn = fn.replace(".", f"_segmentation_{method}.")
        fn = "result_" + fn
        path2segmap = os.path.join(result_root, fn)
        success = utils.save_image(path2segmap, result)
        duration = time.time() - start
        if success:
            print(f"Done in {round(duration, 3)} seconds.")
            print(f"Save segmentation map to {path2segmap}.")
        else:
            print(f"Failed to save segmentation map to {path2segmap}.")


def segment_multiple_images_multiple_directory(configs: Configs):
    image_roots = configs.image.root
    for root in image_roots:
        if not os.path.exists(root):
            print(f"Cannot find folder {root}")
            continue
        segment_multiple_images_one_directory(configs, root)

