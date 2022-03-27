
r"""
Meanshift algorithm to cluster data points into multiple categories.

author:
    Yiqun Chen
"""


import numpy as np


class Kernel:
    def __init__(self) -> None:
        pass

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.value(x)

    def value(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError("NotImplementedError")

    def grad(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError("NotImplementedError")


def gaussian(x: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * (x.T @ x))


def grad_gaussian(x: np.ndarray) -> np.ndarray:
    return -x * gaussian(x)


class Gaussian(Kernel):
    def value(self, x: np.ndarray) -> np.ndarray:
        return gaussian(x)

    def grad(self, x: np.ndarray, scalar: bool=True) -> np.ndarray:
        if scalar:
            return - self(x)
        else:
            return grad_gaussian(x)

