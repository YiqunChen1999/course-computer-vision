
r"""
Histogram calculator.

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("configs/default.py", ""))
import argparse

from cv.utilities.configs import Configs
from cv.utilities.env import overwrite_configs_from_yaml

platform = sys.platform
EXECUTABLE = "main.exe" if "win" in platform else "main"
PATH2MAIN = os.path.abspath(sys.argv[0])
if "win" in platform:
    ROOT = PATH2MAIN.replace(f"cv\\{os.path.basename(PATH2MAIN)}", "") \
        if PATH2MAIN.endswith(".py") else PATH2MAIN.replace(EXECUTABLE, "")
else:
    ROOT = PATH2MAIN.replace(f"cv/{os.path.basename(PATH2MAIN)}", "") \
        if PATH2MAIN.endswith(".py") else PATH2MAIN.replace(EXECUTABLE, "")


parser = argparse.ArgumentParser()
parser.add_argument("--id", type=str, default="deploy")
parser.add_argument("--speedup", action="store_true")
parser.add_argument("--parallel", action="store_true")
parser.add_argument("--workers", type=int, default=None)
args = parser.parse_args()

configs = Configs()

configs.general = Configs()
configs.general.root = ROOT
configs.general.platform = platform
configs.general.id = args.id
configs.general.tasks = [
    "segmentation.threshold", 
    "segmentation.local_threshold", 
    "segmentation.meanshift", 
]

configs.image = Configs()
configs.image.filetype = ["png", "jpg", "jpeg"]
configs.image.root = [
    os.path.join(configs.general.root, "images"), 
    configs.general.root, 
]

configs.result = Configs()
configs.result.root = os.path.join(
    configs.general.root, 
    "results", 
    # "" if configs.general.id == "deploy" else configs.general.id,
)

configs.segmentation = Configs()
configs.segmentation.method = "meanshift" #"local_threshold"
configs.segmentation.threshold = Configs()
configs.segmentation.threshold.bins = 2
configs.segmentation.threshold.thre = "auto"
configs.segmentation.threshold.patches = (4, 4) # (num_rows, num_cols)
configs.segmentation.meanshift = Configs()
configs.segmentation.meanshift.kernel = "Gaussian"
configs.segmentation.meanshift.bandwidth = 92
configs.segmentation.meanshift.tolerance = 5.0
configs.segmentation.meanshift.max_iters = 400
configs.segmentation.meanshift.speedup = args.speedup
configs.segmentation.meanshift.parallel = args.parallel
configs.segmentation.meanshift.workers = args.workers

configs.detection = Configs()
configs.detection.edge = Configs()
configs.detection.corner = Configs()

configs.logs = Configs()
configs.logs.root = os.path.join(
    configs.general.root, "logs", configs.general.id
)
configs.logs.path2log = os.path.join(configs.logs.root, "log.txt")

configs = overwrite_configs_from_yaml(configs)
configs.segmentation.meanshift.speedup = args.speedup
configs.segmentation.meanshift.parallel = args.parallel
configs.convert_state(read_only=True)
