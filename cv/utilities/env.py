
r"""
Environment utilities.

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("utilities/env.py", ""))

import argparse
from copy import deepcopy as dcp

from cv.utilities.configs import Configs


def get_args():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args


def check_env(configs: Configs):
    directories = list()
    directories.extend(dcp(configs.image.root))
    directories.append(configs.result.root)
    for path in directories:
        check_directory(path)


def check_directory(root: os.PathLike):
    if not os.path.exists(root):
        print(f"Cannot find directory {root}, make it now.")
        os.makedirs(root)


def check_file(path: os.PathLike):
    if not os.path.exists(path):
        print(f"Cannot find directory {path}.")


def print_info():
    cols, _ = os.get_terminal_size(0)
    half = (cols - 6) // 2
    print("=" * half + " INFO " + "=" * half)
