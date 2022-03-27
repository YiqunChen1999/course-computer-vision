
r"""
Meanshift algorithm to cluster data points into multiple categories.

author:
    Yiqun Chen
"""


import numpy as np

from cv.ops.cluster import Cluster, KNearestNeighbors
from cv.ops.kernel import Kernel

class MeanShift(Cluster):
    def __init__(
        self, 
        kernel: Kernel, 
        bandwidth: float, 
        bins: int=None,
        tolerance: float=1.0,  
        eps: float=1e-6, 
        max_iters: int=400, 
    ) -> None:
        super().__init__(max_iters)
        self.kernel = kernel
        self.bandwidth = bandwidth
        self.bins = bins
        self.tolerance = tolerance
        self.eps = eps

    def fit(self, data: np.ndarray, label: np.ndarray=None):
        r"""
        Fit the data.

        Args:
            data: (num_samples, num_features).
            label: not used.

        Returns:
        """
        assert len(data.shape) == 2, data.shape
        # Fit the data.
        if self.bins is None:
            self.bins = data.shape[0]
        _centers_idx = np.random.choice(
            data.shape[0], self.bins, replace=False
        )
        self._centers = data[_centers_idx, :]

        for it in range(self.max_iters):
            differences = self._centers[:, np.newaxis, :] \
                            - data[np.newaxis, :, :]
            assert differences.shape == (
                self.num_clusters, data.shape[0], self.num_features
            ), differences.shape
            distances = np.sum(differences ** 2, axis=-1)
            points_in_ball = distances <= self.bandwidth**2
            for center_idx in range(self.num_clusters):
                points = data[points_in_ball[center_idx], :]
                center = np.mean(points, axis=0, keepdims=True)
                assert center.shape == (1, self.num_features), center.shape
                self._centers[center_idx] = center
            # Merge clusters.
            self._merge_clusters()

    def _merge_clusters(self):
        differences = self._centers[np.newaxis, :, :] \
                      - self._centers[:, np.newaxis, :]
        distances = np.sqrt(np.linalg.norm(differences, axis=-1))
        centers = []
        merged_clusters = []
        for center_idx in range(self.num_clusters):
            if center_idx in merged_clusters:
                continue
            nearby_clusters = distances[center_idx] <= self.tolerance
            centers.append(np.mean(
                self._centers[nearby_clusters], axis=0, keepdims=True
            ))
            merged_clusters.extend(np.nonzero(nearby_clusters)[0].tolist())
        self._centers = np.concatenate(centers, axis=0)

    def predict(self, data: np.ndarray) -> np.ndarray:
        assert len(data.shape) == 2, data.shape
        if data.shape[1] != self.num_features:
            raise RuntimeError(
                f"Expect number of features is {self.num_features}, "
                f"but got {data.shape[1]}."
            )
        # return KNearestNeighbors(1)(self.centers)(data)
        neareast_neighbors = KNearestNeighbors(1)
        neareast_neighbors.fit(self._centers)
        return neareast_neighbors(data)

