

r"""
author:
    Yiqun Chen

docs: 
    Visualizer to visualize some attributes.
"""

import os
import numpy as np
import matplotlib.pyplot as plt



def plot_color_distribution(image: np.ndarray, path2save: os.PathLike):
    if not os.path.exists(os.path.dirname(path2save)):
        os.makedirs(os.path.dirname(path2save))
    assert len(image.shape) == 2, image.shape
    assert image.shape[-1] in [1, 3], image.shape
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    if image.shape[-1] == 1:
        ax.scatter(image, image, image, marker="o")
    else:
        ax.scatter(image[:, 0], image[:, 1], image[:, 2], marker="o")
    ax.set_xlabel('R')
    ax.set_ylabel('G')
    ax.set_zlabel('B')
    plt.show()
    plt.savefig(path2save)


