
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
    assert isinstance(configs.image, Configs)
    assert configs.image.type == ["png", "jpg", "jpeg"]
    assert configs["image"] is configs.image
    assert configs["image"].type is configs.image.type
    configs.folder = "./"
