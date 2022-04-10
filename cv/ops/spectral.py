

import os
from typing import Any

from cv.utilities.init import INITIALIZER
import numpy as np

from cv.ops.cluster import Cluster
from cv.ops.kmeans import KMeans
from cv.utilities.utils import loginfo, logstatus

class NormalizedSpectral(Cluster):
    def __init__(
        self, 
        k: int, 
        n_clusters: int, 
        sigma: float, 
        tol: float=1e-6, 
        max_iter: int=100, 
        k_means_initializer: str="initialize_centers_from_multiple_samples", 
        seed: int=2021, 
        verbose: bool=True, 
        path2log: os.PathLike=None, 
    ) -> None:
        super().__init__(max_iter)
        assert k > 0, "Parameter should be positive."
        self.k = k
        self.n_clusters = n_clusters
        self.sigma = sigma
        self.tol = tol
        self.k_means_initializer = k_means_initializer
        self.seed = seed
        self.verbose = verbose
        self.path2log = path2log
        self.k_means = KMeans(
            k=self.n_clusters, 
            tol=self.tol, 
            max_iter=self.max_iter, 
            seed=self.seed, 
            verbose=self.verbose, 
            path2log=self.path2log, 
        )
        loginfo(
            f"Build K-Means Cluster with "
            f"k = {k}, tolerance = {tol}, seed = {seed}", 
            verbose, 
            self.path2log, 
        )

    def forward(self, samples: np.ndarray, verbose: bool=True) -> np.ndarray:
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
        raise NotImplementedError("NotImplemented.")

    def fit(self, samples: np.ndarray, verbose: bool=True):
        r"""
        Fit the k-means model.

        Args:
            samples: Shape(N, D), where N is the number of training samples, 
                D is the dimension of samples.
            verbose: whether to display messages or not.
        
        Returns: 
        """
        N, D = samples.shape
        laplacian = self._calc_laplacian(samples)
        eigvals, eigvecs = np.linalg.eig(laplacian)
        topk_small_idx = np.argsort(eigvals)[: self.k]
        U = eigvecs[:, topk_small_idx]
        U = U / (np.sum(U**2, axis=1, keepdims=True) + self.tol)
        self.k_means.reset_centers(
            INITIALIZER[self.k_means_initializer](
                U, 
                k=self.n_clusters, 
                seed=self.seed, 
            )
        )
        return self.k_means.fit(U, verbose=self.verbose)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.forward(*args, **kwds)

    def _calc_laplacian(self, samples: np.ndarray):
        N, D = samples.shape
        distances = np.sum(
            (samples[:, np.newaxis, :] - samples[np.newaxis])**2, axis=2
        )
        distances = np.exp(-(distances)/(2*self.sigma)) - np.eye(N)
        # Sort along each row (left to right).
        topk = np.argsort(distances, axis=1)[:, -self.k: ]
        weight = np.zeros_like(distances)
        np.put_along_axis(
            weight, 
            topk, 
            np.take_along_axis(distances, topk, axis=1), 
            axis=1, 
        )
        weight = 0.5 * (weight + weight.T)
        degree = np.diag(np.sum(weight, axis=1)**(-0.5))
        laplacian = np.eye(N) - degree @ weight @ degree
        return laplacian
        
