import random
from functools import partial

from scipy.stats import norm

from syntheticdb.db_core import Distribution


def uniform(min: float, max: float) -> Distribution:
    return Distribution(
        sample=lambda: (random.random() * max - min) + min,
        cdf=partial(uniform_cdf, min, max),
    )


def standard_normal(mean: float, std_dev: float) -> Distribution:
    dist = norm(loc=mean, scale=std_dev)
    return Distribution(sample=dist.rvs, cdf=dist.cdf)


def uniform_cdf(min_val: float, max_val: float, point: float) -> float:
    if point < min_val:
        return 0
    if min_val < point < max_val:
        return (point - min_val) / (max_val - min_val)
    if point > max_val:
        return 1
