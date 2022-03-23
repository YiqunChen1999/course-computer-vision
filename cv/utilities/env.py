
r"""
Environment utilities.

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("utilities/env.py", ""))

import argparse


def get_args():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args
