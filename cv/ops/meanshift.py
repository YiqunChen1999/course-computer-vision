
r"""
Meanshift algorithm to cluster data points into multiple categories.

author:
    Yiqun Chen
"""


import os
import time
import numpy as np
import multiprocessing as mp
import ctypes

from cv.ops.cluster import Cluster, KNearestNeighbors
from cv.ops.kernel import Kernel
from cv.utilities.init import INITIALIZER
# from cv.utilities import utils
from cv.utilities.env import loginfo, logstatus


def single_center_meanshift(
    center: np.ndarray, 
    data: np.ndarray, 
    radius: float, 
    max_iters: int, 
    tolerance: float=1e-3, 
) -> np.ndarray:
    r"""
    Executing mean shift for one center, this function is designed
    for parallel executing.

    Args:
        center: (1, num_feats)
        data: (num_samples, num_feats)
        radius:
        max_iters: 
        tolerance: 

    Returns:
        center: (1, num_feats)
    """
    tolerance *= radius
    if len(center.shape) == 1:
        center = center[np.newaxis]
    shape = center.shape
    for it in range(max_iters):
        assert center.shape == shape, center.shape
        old_center = center.copy()
        diffs = center[np.newaxis] - data[:, np.newaxis, :]
        distances = np.linalg.norm(diffs, axis=2) # (num_samples, 1)
        points_in_ball = (distances < radius)[:, 0] # (num_samples, )
        if not np.any(points_in_ball):
            break
        center = np.mean(data[points_in_ball], axis=0, keepdims=True)
        center_diff = np.linalg.norm(center - old_center)
        if center_diff < tolerance:
            break
    return center


class MeanShift(Cluster):
    def __init__(
        self, 
        kernel: Kernel, 
        bandwidth: float, 
        num_seeds: int=None,
        tolerance: float=1.0,  
        speedup: bool=False, 
        parallel: bool=False, 
        eps: float=1e-6, 
        max_iters: int=400, 
        init_method: str="initialize_centers_from_histogram", 
        num_tasks: int=None, 
    ) -> None:
        super().__init__(max_iters)
        self.kernel = kernel
        self.bandwidth = bandwidth
        self.num_seeds = num_seeds
        self.tolerance = tolerance
        self.speedup = speedup
        self.parallel = parallel
        self.eps = eps
        self.init_method = init_method
        self.num_tasks = num_tasks

    def fit(self, data: np.ndarray, label: np.ndarray=None):
        r"""
        Fit the data.

        Args:
            data: (num_samples, num_features).
            label: not used.

        Returns:
        """
        self._before_fit(data, label)
        if self.parallel:
            self._parallel_fit(data, label)
        else:
            self._single_fit(data, label)

        self._merge_clusters()
        logstatus(
            self._fitting_message_template.format(
                self.num_clusters, 100
            ), 
            newline=True, 
        )
        loginfo(f"Produce {self.num_clusters} clusters.")

    def _single_fit(self, data: np.ndarray, label: np.ndarray=None):
        ctr_idx = 0
        while ctr_idx < self.num_clusters:
            # Executing test.
            self._centers[ctr_idx] = single_center_meanshift(
                self._centers[ctr_idx, ...], 
                data, 
                self.bandwidth, 
                self.max_iters, 
            )
            ctr_idx += 1
            logstatus(
                self._fitting_message_template.format(
                    self.num_clusters, 
                    100 * np.round(ctr_idx / self.num_clusters, 4), 
                ), 
            )
            if self.speedup:
                self._merge_clusters()

    def _parallel_fit(self, data: np.ndarray, label: np.ndarray=None):
        shared_data = mp.Array(ctypes.c_double, data.size)
        shared_data = np.frombuffer(shared_data.get_obj())
        shared_data = shared_data.reshape(data.shape)
        shared_data[:] = data[:]
        with mp.Pool(os.cpu_count()) as executor:
            centers = executor.starmap_async(
                single_center_meanshift, 
                zip(
                    self._centers, 
                    [shared_data] * self.num_clusters, 
                    [self.bandwidth] * self.num_clusters, 
                    [self.max_iters] * self.num_clusters, 
                )
            )
            while True:
                if centers.ready():
                    break
                remaining = centers._number_left * centers._chunksize
                completed = self.num_clusters - remaining
                logstatus(
                    self._fitting_message_template.format(
                        self.num_clusters, 
                        100 * np.round(completed / self.num_clusters, 4), 
                    ), 
                )
                time.sleep(0.5)
            centers = centers.get()
        centers = np.concatenate(centers)
        self._merge_clusters()

    def _merge_clusters(self):
        ctr_idx = 0
        while ctr_idx < self.num_clusters:
            # Calculate distances.
            diff = self._centers[ctr_idx][np.newaxis] - self._centers
            assert len(diff.shape) == 2, diff.shape
            assert len(diff) == self.num_clusters, diff.shape
            dist = np.sqrt(np.linalg.norm(diff, axis=1))
            similar_ids = dist <= self.tolerance
            unsimilar_ids = dist > self.tolerance
            if not np.any(similar_ids):
                continue
            new_center = np.mean(
                self._centers[similar_ids], axis=0, keepdims=True
            )
            self._centers = np.concatenate(
                [new_center, self._centers[unsimilar_ids]], axis=0
            )
            assert len(self.shape) == 2, self.shape
            ctr_idx += 1

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

    def _before_fit(self, data: np.ndarray, label: np.ndarray=None):
        self._fitting_message_template = \
            "[ Mean Shift Fitting ]" \
            + "[ Clusters {:>8} ]" \
            + "[ Progress {:<4.02f} % ]"
        assert len(data.shape) == 2, data.shape
        num_samples, num_feats = data.shape
        if self.num_seeds is None:
            self.num_seeds = data.shape[0]
        self._centers = INITIALIZER[self.init_method](data, self.num_seeds)

        # Execute tasks parallel until convergence or reach max iters.
        loginfo(f"Number of clusters: {self.num_clusters}")
        if self.speedup:
            loginfo(
                "You are using * FAST * mode, " \
                + "set configs-segmentation-meanshift-speedup " \
                + "as false in 'configs/default.yml' to cancel it."
            )
        else:
            loginfo(
                "set configs-segmentation-meanshift-speedup " \
                + "as true in 'configs/default.yml' " \
                + "can speedup segmentation."
            )
