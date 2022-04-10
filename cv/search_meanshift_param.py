
r"""
Main function to process image(s).

author: 
    Yiqun Chen
"""
# __package__ = __file__
import os
import sys
sys.path.append(__file__.replace("cv/main.py", ""))

from cv.utilities.configs import Configs
from cv.task.segmentation import segment_multiple_images_multiple_directory
from cv.utilities.env import check_env, print_info, backup_configs

INFO = "SEARCH MEANSHIFT PARAMS"
RANGE = {
    "BANDWIDTH": range(10, 96), 
    "SEEDS": (1000, 10000), 
    "TOLERANCE": [0.1, 0.5] + [1.0 + 0.5 * i for i in range(16)], 
}

def main(configs: Configs):
    check_env(configs)
    for task in configs.general.tasks:
        if task.split(".")[0] == "segmentation":
            segment_multiple_images_multiple_directory(configs, task)


if __name__ == "__main__":
    print_info(INFO)
    from cv.configs.default import configs
    print(RANGE)
    RANGE["TOLERANCE"].reverse()
    for bandwidth in RANGE["BANDWIDTH"]:
        for num_seeds in RANGE["SEEDS"]:
            for tolerance in RANGE["TOLERANCE"]:
                configs.convert_state(read_only=False)
                configs.segmentation.meanshift.bandwidth = bandwidth
                configs.segmentation.meanshift.num_seeds = num_seeds
                configs.segmentation.meanshift.tolerance = tolerance
                configs.convert_state(read_only=True)
                print(configs)
                main(configs)
                name = f"bw{bandwidth}-ns{num_seeds}-tol{tolerance}"
                backup_configs(configs, name)
    print_info(INFO)
