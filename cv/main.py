
r"""
Main function to process image(s).

author: 
    Yiqun Chen
"""
# __package__ = __file__
import os
import sys
sys.path.append(__file__.replace("cv/main.py", ""))
import multiprocessing as mp

from cv.utilities.configs import Configs
from cv.task.segmentation import segment_multiple_images_multiple_directory
from cv.utilities.env import check_env, print_info, backup_configs

def main(configs: Configs):
    for task in configs.general.tasks:
        if task.split(".")[0] == "segmentation":
            segment_multiple_images_multiple_directory(configs, task)


if __name__ == "__main__":
    from cv.configs.default import configs
    if "win" in configs.general.platform:
        mp.set_start_method("spawn")
    else:
        mp.set_start_method("fork")
    check_env(configs)
    print_info()
    print(configs)
    main(configs)
    backup_configs(configs)
    print_info()
