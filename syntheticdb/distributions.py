from scipy.stats import uniform
from scipy.stats import norm
## 
from syntheticdb.db_core import Distribution


def Uniform(min: float, max: float) -> Distribution:
    dist = uniform(loc=min, scale=max-min)
    return Distribution(sample=dist.rvs, cdf=dist.cdf)

def Normal(mean: float, std_dev: float) -> Distribution:
    dist = norm(loc=mean, scale=std_dev)
    return Distribution(sample=dist.rvs, cdf=dist.cdf)
