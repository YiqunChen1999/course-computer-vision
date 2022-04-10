

from typing import Union, Iterable
import numpy as np


INITIALIZER = {}
def register_initializer(fn):
    INITIALIZER[fn.__name__] = fn
    return fn


@register_initializer
def initialize_centers_randomly(
    data: np.ndarray, k: int, seed: int=None
) -> np.ndarray:
    N, D = data.shape
    np.random.seed(seed)
    centers = np.random.randn(k, D)
    return centers


@register_initializer
def initialize_centers_from_data_uniformly(
    data: np.ndarray, k: int, seed: int=None
) -> np.ndarray:
    N, D = data.shape
    np.random.seed(seed)
    shift = np.random.randint(low=0, high=np.floor(N/k)-1)
    indices = np.array(list(range(0, N, N//k))) + shift
    return data[indices]


@register_initializer
def initialize_centers_from_data_randomly(
    data: np.ndarray, k: int, seed: int=None
) -> np.ndarray:
    N, D = data.shape
    np.random.seed(seed)
    indices = np.random.choice(np.arange(N), k, False)
    return data[indices]


@register_initializer
def initialize_centers_from_multiple_samples(
    data: np.ndarray, 
    k: int, 
    seed: int=None, 
    n_samples: int=None, 
    replace: bool=False, 
) -> np.ndarray:
    N, D = data.shape
    np.random.seed(seed)
    if n_samples is None:
        n_samples = int(np.floor(N/k))

    # Choose n_samples for each cluster center.
    indices = np.random.choice(
        np.cumsum(np.ones(N, dtype=int))-1, size=n_samples*k, replace=replace
    )
    centers = np.mean(data[indices].reshape(k, n_samples, -1), axis=1)
    return centers


@register_initializer
def initialize_centers_from_histogram_uniformly(
    data: np.ndarray, 
    k: int, 
    seed: int=None, 
    # n_samples: int=None, 
    # replace: bool=False, 
    bins: Union[int, Iterable[int]]=4, 
) -> np.ndarray:
    r"""
    Initialize the centers by sampling from histogram uniformly.
    """
    N, D = data.shape
    np.random.seed(seed)
    if not isinstance(bins, Iterable):
        bins = (bins, ) * D
    hist, edge = np.histogramdd(data, bins)
    k_per_block = np.zeros(hist.size, dtype=np.int32) + k // hist.size
    ids = np.random.choice(hist.size, k - k % hist.size, replace=False)
    k_per_block[ids] += 1
    centers = []
    ids_map = np.arange(hist.size).reshape(bins)
    for block_idx in range(hist.size):
        edge_idx = np.nonzero(ids_map == block_idx)
        low = np.array([[e[i] for e, i in zip(edge, edge_idx)]])
        high = np.array([[e[i] for e, i in zip(edge, edge_idx)]])
        points_in_block = (data < high) & (data > low)
        k_in_block = k_per_block[block_idx]
        replace = True if points_in_block.sum() < k_in_block else False
        sampled_centers = np.random.choice(
            data[points_in_block, :], 
            size=k_per_block[block_idx], 
            replace=replace, 
        )
        if len(sampled_centers.shape) == 1:
            sampled_centers = sampled_centers[np.newaxis]
        centers.append(sampled_centers)
    return np.concatenate(centers, axis=0)



@register_initializer
def initialize_centers_from_histogram(
    data: np.ndarray, 
    k: int, 
    seed: int=None, 
    bins: Union[int, Iterable[int]]=4, 
) -> np.ndarray:
    r"""
    Initialize the centers by sampling from 
    """
    N, D = data.shape
    np.random.seed(seed)
    if not isinstance(bins, Iterable):
        bins = (bins, ) * D
    hist, edge = np.histogramdd(data, bins)
    ids_map = np.arange(hist.size).reshape(bins)
    nonempty_block = hist != 0
    nonempty_block_ids = ids_map[np.nonzero(nonempty_block)]
    prob = hist / hist.sum()
    k_per_block = np.zeros(hist.size, dtype=np.int32)
    k_per_block[nonempty_block_ids] += 1
    position, counts = np.unique(
        np.random.choice(
            hist.size, 
            size=k - k_per_block.sum(), 
            p=prob.reshape(-1), 
        ), 
        return_counts=True, 
    )
    k_per_block[position] += counts
    assert k_per_block.sum() == k

    # Sampling centers from data.
    centers = []
    for block_idx in range(hist.size):
        if k_per_block[block_idx] == 0:
            continue
        edge_idx = np.nonzero(ids_map == block_idx)
        low = np.concatenate(
            [e[i] for e, i in zip(edge, edge_idx)]
        )[np.newaxis]
        high = np.concatenate(
            [e[i+1] for e, i in zip(edge, edge_idx)]
        )[np.newaxis]
        points_in_block = (data <= high) & (data >= low)
        points_in_block = points_in_block.sum(axis=1) == D
        k_in_block = k_per_block[block_idx]
        assert points_in_block.sum(), points_in_block.sum()
        replace = True if points_in_block.sum() < k_in_block else False
        sampled_centers_ids = np.random.choice(
            np.nonzero(points_in_block)[0], 
            size=k_in_block, 
            replace=replace, 
        )
        sampled_centers = data[sampled_centers_ids]
        if len(sampled_centers.shape) == 1:
            sampled_centers = sampled_centers[np.newaxis]
        centers.append(sampled_centers)
    centers = np.concatenate(centers, axis=0)
    assert len(centers) == k, centers.shape
    return centers



