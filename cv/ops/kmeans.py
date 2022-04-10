
import os
from typing import Any
from copy import deepcopy as dcp
import numpy as np

from cv.ops.cluster import Cluster
from cv.utilities.utils import loginfo, logstatus

class KMeans(Cluster):
    def __init__(
        self, 
        k: int, 
        tol: float=1e-6, 
        max_iter: int=100, 
        seed: int=2021, 
        verbose: bool=True, 
        path2log: os.PathLike=None, 
    ) -> None:
        super().__init__()
        assert k > 0, "Parameter should be positive."
        self.k = k
        self.max_iter = max_iter
        self.tol = tol
        self.seed = seed
        self._centers = None
        self.path2log = path2log
        loginfo(
            f"Build K-Means Cluster with "
            f"k = {k}, tolerance = {tol}, seed = {seed}", 
            verbose, 
            self.path2log, 
        )

    def predict(self, samples: np.ndarray) -> np.ndarray:
        r"""
        Find a cluster for the given samples.

        Args:
            samples: Shape(N, D), N is the number of input samples, 
                D is the dimension of input samples.
        
        Returns:
            : a vector with each element indicates the cluster.
        """
        if self._centers is None:
            raise RuntimeError(
                "Please call `fit` method first."
            )
        distances = self._centers @ samples.T
        labels = np.argmin(distances, axis=0)

    def reset_centers(self, centers: np.ndarray):
        self._centers = centers

    def fit(self, data: np.ndarray, label: np.ndarray=None):
        r"""
        Fit the k-means model.

        Args:
            data: Shape(N, D), where N is the number of training samples, 
                D is the dimension of samples.
            verbose: whether to display messages or not.
        
        Returns: 
        """
        if self._centers is None:
            raise RuntimeError(
                "Please call `reset_centers` method first."
            )
        N, D = data.shape

        # delta is the L2 norm of shift of centers.
        delta = 1.0
        cnt_iter = 0
        while delta > self.tol and cnt_iter < self.max_iter:
            old_centers = dcp(self._centers)
            distances = np.linalg.norm(
                self._centers[:, np.newaxis, :] - data[np.newaxis], axis=2
            )
            labels = np.argmin(distances, axis=0)

            # Update the centers of each cluster.
            for idx in range(self.k):
                self._centers[idx] = \
                    np.mean(data[labels==idx], axis=0)
            shift = self._centers - old_centers
            delta = np.max(np.linalg.norm(shift, axis=1))
            cnt_iter += 1
        self.labels = labels

