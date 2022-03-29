
r"""
Histogram calculator.

author: 
    Yiqun Chen
"""

from ctypes import Union
import os
import sys

sys.path.append(__file__.replace("test/utilities/test_configs.py", ""))


from cv.utilities.configs import Configs


def test_configs():
    configs = Configs(image=Configs())
    configs.image.type = ["png", "jpg", "jpeg"]
    configs.segmentation.method = "threshold"
    assert configs.segmentation.method == "threshold", cfg
    cfg = {
        "segmentation": {
            "method": "meanshift", 
            "meanshift": {
                "bins": 0.1, 
                "patches": (4, 4), 
            }
        }
    }
    cfg = Configs(cfg)
    configs = configs.cvt2dict()
    assert "segmentation" in configs.keys(), configs.keys()
    configs.update(cfg)
    assert "segmentation" in configs.keys(), configs.keys()
    configs = Configs(configs)
    assert configs.segmentation.method == "meanshift", cfg
    assert "segmentation" in configs.keys(), configs.keys()
    # assert "method" in cfg.segmentation
    # assert "meanshift" in cfg.segmentation
    # assert "bins" in cfg.segmentation.meanshift
    assert isinstance(configs.image, Configs)
    assert configs.image.type == ["png", "jpg", "jpeg"]
    assert configs["image"] is configs.image
    assert configs["image"].type is configs.image.type
    configs.folder = "./"
