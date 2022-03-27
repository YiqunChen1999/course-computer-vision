
r"""
Histogram calculator.

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("configs/default.py", ""))

from cv.utilities.configs import Configs

PATH2MAIN = os.path.abspath(sys.argv[0])
ROOT = PATH2MAIN.replace("cv/main.py", "") \
    if PATH2MAIN.endswith("main.py") else PATH2MAIN.replace("main", "")


configs = Configs()

configs.general = Configs()
configs.general.root = ROOT
configs.general.tasks = ["segmentation"]

configs.image = Configs()
configs.image.filetype = ["png", "jpg", "jpeg"]
configs.image.root = [
    os.path.join(configs.general.root, "images"), 
    configs.general.root, 
]

configs.result = Configs()
configs.result.root = os.path.join(configs.general.root, "results")

configs.segmentation = Configs()
configs.segmentation.method = "meanshift" #"local_threshold"
configs.segmentation.threshold = Configs()
configs.segmentation.threshold.bins = 2
configs.segmentation.threshold.thre = "auto"
configs.segmentation.threshold.patches = (4, 4) # (num_rows, num_cols)
configs.segmentation.meanshift = Configs()
configs.segmentation.meanshift.kernel = "Gaussian"
configs.segmentation.meanshift.bandwidth = 4
configs.segmentation.meanshift.bins = 10
configs.segmentation.meanshift.tolerance = 1e-1
configs.segmentation.meanshift.max_iters = 400
configs.segmentation.meanshift.patches = (4, 4) # (num_rows, num_cols)

configs.detection = Configs()
configs.detection.edge = Configs()
configs.detection.corner = Configs()

