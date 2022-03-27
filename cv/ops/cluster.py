
r"""
Meanshift algorithm to cluster data points into multiple categories.

author:
    Yiqun Chen
"""


import numpy as np


class Cluster:
    def __init__(self, max_iters: int=400) -> None:
        self.max_iters = max_iters
        self._centers: np.ndarray = np.zeros((0, 0))

    @property
    def centers(self) -> np.ndarray:
        r"""The vectors of centers, with shape (NumCenters, NumFeatures)"""
        return self._centers.copy()

    @property
    def shape(self) -> tuple:
        return self._centers.shape

    @property
    def num_clusters(self) -> int:
        return self._centers.shape[0]

    @property
    def num_features(self) -> int:
        return self._centers.shape[1]

    def fit(self, data: np.ndarray, label: np.ndarray=None):
        raise NotImplementedError("NotImplementedError")

    def predict(self, data: np.ndarray) -> np.ndarray:
        raise NotImplementedError("NotImplementedError")

    def __call__(self, data: np.ndarray) -> np.ndarray:
        return self.predict(data)


class KNearestNeighbors(Cluster):
    def __init__(self, k: int, max_iters: int=None) -> None:
        super().__init__(max_iters)
        self.k = k
        assert k > 0, k
        self._centers = np.zeros((k, 0))

    def fit(self, centers: np.ndarray, label: np.ndarray=None):
        # assert centers.shape[0] == self.num_clusters, centers.shape
        self._centers = centers

    def predict(self, data: np.ndarray) -> np.ndarray:
        difference = data[:, np.newaxis, :] \
                        - self._centers[np.newaxis, :, :]
        distances = np.linalg.norm(difference, axis=-1)
        assert tuple(distances.shape) == (data.shape[0], self.num_clusters)
        label = np.argmax(distances, axis=-1)
        return label

