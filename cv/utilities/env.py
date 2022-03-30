
r"""
Environment utilities.

author: 
    Yiqun Chen
"""

import os
import sys
from typing import Mapping, Union

sys.path.append(__file__.replace("utilities/env.py", ""))

import argparse
from copy import deepcopy as dcp
import yaml

from cv.utilities.configs import Configs


def get_args():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args


def overwrite_configs_from_yaml(
    configs: Configs, path2yaml: os.PathLike=None
) -> Configs:
    if path2yaml is None:
        path2yaml = os.path.join(
            configs.general.root, "configs", "default.yml"
        )
    if not os.path.exists(path2yaml):
        return configs
    with open(path2yaml, 'r') as fp:
        configs_yaml = yaml.safe_load(fp)["configs"]
    configs.merge_from(configs_yaml)
    return configs


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
