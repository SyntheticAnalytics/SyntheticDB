from scipy.stats import uniform
from scipy.stats import norm
from scipy.stats import loguniform
from scipy.stats import lognorm
from scipy.stats import gamma
from scipy.stats import expon
from scipy.stats import beta
from scipy.stats import weibull_min
## 
from syntheticdb.db_core import Distribution

## helper fn
def makeDistribution(dist) -> Distribution:
    return Distribution(sample=dist.rvs, cdf=dist.cdf)

## distributions ##

def Uniform(loc: float, scale: float) -> Distribution:
    dist = uniform(loc=loc, scale=scale)
    return makeDistribution(dist)

def LogUniform(a: float, b: float) -> Distribution:
    dist = loguniform(a=a,b=b)
    return makeDistribution(dist)

def Normal(loc: float, scale: float) -> Distribution:
    dist = norm(loc=loc, scale=scale)
    return makeDistribution(dist)

def LogNormal(s: float, loc: float, scale: float) -> Distribution:
    dist = lognorm(s=s, loc=loc, scale=scale)
    return makeDistribution(dist)

def Gamma(a: float, loc: float, scale: float) -> Distribution:
    dist = gamma(a=a, loc=loc, scale=scale)
    return makeDistribution(dist)

def Exponential(loc: float, scale: float) -> Distribution:
    dist = expon(loc=loc, scale=scale)
    return makeDistribution(dist)

def Beta(a: float, b: float) -> Distribution:
    dist = beta(a=a, b=b)
    return makeDistribution(dist)

def Weibull(c: float, loc: float, scale: float) -> Distribution:
    dist = weibull_min(c=c, loc=loc, scale=scale)
    return makeDistribution(dist)

