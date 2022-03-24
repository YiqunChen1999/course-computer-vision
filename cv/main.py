
r"""
Main function to process image(s).

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("cv/main.py", ""))

from cv.utilities.configs import Configs
from cv.task.segmentation import segment_multiple_images

def main(configs: Configs):
    for task in configs.general.tasks:
        if task == "segmentation":
            segment_multiple_images(configs)


if __name__ == "__main__":
    from cv.configs.default import configs
    main(configs)
