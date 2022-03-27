
r"""
Histogram calculator.

author: 
    Yiqun Chen
"""

import os
import sys
sys.path.append(__file__.replace("utilities/configs.py", ""))
__package__ = ".utilities.configs"

from typing import Any

from collections import UserDict


class Configs(UserDict):
    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def __getattr__(self, name: str):
        return self[name]
