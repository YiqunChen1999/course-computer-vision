
r"""
Histogram calculator.

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("configs/default.py", ""))

from cv.utilities.configs import Configs


configs = Configs()

configs.general = Configs()
configs.general.root = __file__.replace("cv/configs/default.py", "")
configs.general.tasks = ["segmentation"]

configs.image = Configs()
configs.image.filetype = ["png", "jpg", "jpeg"]
configs.image.root = os.path.join(configs.general.root, "images")

configs.result = Configs()
configs.result.root = os.path.join(configs.general.root, "results")

configs.segmentation = Configs()
configs.segmentation.method = "threshold"
configs.segmentation.threshold = Configs()
configs.segmentation.threshold.bins = 2
configs.segmentation.threshold.thre = "auto"

configs.detection = Configs()
configs.detection.edge = Configs()
configs.detection.corner = Configs()

