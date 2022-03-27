
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
from cv.utilities.env import check_env, print_info

def main(configs: Configs):
    check_env(configs)
    for task in configs.general.tasks:
        if task == "segmentation":
            segment_multiple_images_multiple_directory(configs)


if __name__ == "__main__":
    print_info()
    from cv.configs.default import configs
    main(configs)
    print_info()
