
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


def log2file(
    message: str, 
    path2file: os.PathLike="./logs/log.txt", 
    *args, 
    **kwargs, 
):
    with open(path2file, 'a') as fp:
        print(message, file=fp, *args, **kwargs)


def loginfo(info: str, *args, **kwargs):
    message = "[ INFO ] " + info
    print(message)
    log2file(message)


def logstatus(status: str, newline=False, *args, **kwargs):
    cols, _ = os.get_terminal_size(0)
    end = "\n" if newline else ""
    message = "\r" + " " * cols + "\r" + "[ INFO ] " + status
    print(message, end=end)
    log2file(message, end=end)


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
    directories.append(configs.logs.root)
    for path in directories:
        check_directory(path)


def backup_configs(configs: Configs, name: str="") -> bool:
    loginfo("Backup configs and results.")
    root = configs.general.root
    expr = configs.general.id
    src = os.path.join(root, "configs")
    des = configs.result.root
    os.system(f"cp -r {src} {des}")
    if name == "":
        src = os.path.join(configs.logs.root, f"{expr}.tar.gz")
    else:
        src = os.path.join(configs.logs.root, f"{expr}-{name}.tar.gz")
    des = "./results"
    loginfo(f"Backup file: {src}")
    os.system(f"tar -zcvf {src} {des}")


def check_directory(root: os.PathLike):
    if not os.path.exists(root):
        print(f"Cannot find directory {root}, make it now.")
        os.makedirs(root)


def check_file(path: os.PathLike):
    if not os.path.exists(path):
        print(f"Cannot find directory {path}.")


def print_info(info: str="INFO"):
    cols, _ = os.get_terminal_size(0)
    half = (cols - len(info) - 2) // 2
    message = "=" * half + f" {info} " + "=" * half
    print(message)
    log2file(message)

