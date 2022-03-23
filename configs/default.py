
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

configs.image = Configs()

configs.segmentation = Configs()
configs.segmentation.method = "histogram"

configs.detection = Configs()

configs.detection.edge = Configs()

configs.detection.corner = Configs()
