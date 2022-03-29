
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


def merge_configs(
    configs: Union[Configs, dict], 
    another: Union[Configs, dict], 
) -> Configs:
    if isinstance(configs, Configs):
        configs = dcp(configs).cvt2dict()
    if isinstance(another, Configs):
        another = dcp(another).cvt2dict()
    for key, val in another.items():
        if key not in configs.keys():
            configs[key] = val
        elif isinstance(val, dict) \
                and isinstance(configs[key], dict):
            cfg = merge_configs(configs[key], val).cvt2dict()
            configs[key] = cfg
        else:
            configs[key] = val
    return Configs(configs)


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
        configs_yaml = yaml.load(fp, yaml.Loader)["configs"]
    configs = merge_configs(configs, configs_yaml)
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
