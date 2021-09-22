import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats
import pandas as pd

size = 30000
x = np.arange(size)
y = scipy.int_(np.round_(scipy.stats.vonmises.rvs(5, size=size) * 47))
h = plt.hist(y, bins=range(48))
all_dist_names = [
    "alpha",
    "anglit",
    "arcsine",
    "beta",
    "betaprime",
    "bradford",
    "burr",
    "cauchy",
    "chi",
    "chi2",
    "cosine",
    "dgamma",
    "dweibull",
    "erlang",
    "expon",
    "exponweib",
    "exponpow",
    "f",
    "fatiguelife",
    "fisk",
    "foldcauchy",
    "foldnorm",
    "frechet_r",
    "frechet_l",
    "genlogistic",
    "genpareto",
    "genexpon",
    "genextreme",
    "gausshyper",
    "gamma",
    "gengamma",
    "genhalflogistic",
    "gilbrat",
    "gompertz",
    "gumbel_r",
    "gumbel_l",
    "halfcauchy",
    "halflogistic",
    "halfnorm",
    "hypsecant",
    "invgamma",
    "invgauss",
    "invweibull",
    "johnsonsb",
    "johnsonsu",
    "ksone",
    "kstwobign",
    "laplace",
    "logistic",
    "loggamma",
    "loglaplace",
    "lognorm",
    "lomax",
    "maxwell",
    "mielke",
    "nakagami",
    "ncx2",
    "ncf",
    "nct",
    "norm",
    "pareto",
    "pearson3",
    "powerlaw",
    "powerlognorm",
    "powernorm",
    "rdist",
    "reciprocal",
    "rayleigh",
    "rice",
    "recipinvgauss",
    "semicircular",
    "t",
    "triang",
    "truncexpon",
    "truncnorm",
    "tukeylambda",
    "uniform",
    "vonmises",
    "wald",
    "weibull_min",
    "weibull_max",
    "wrapcauchy",
]
dist_names = ["lognorm", "gamma", "beta", "rayleigh", "norm", "pareto"]
# %%


class Distributions:
    def __init__(self, dist_names):

        self.dist_names = dist_names
        self.dists = {}

        self.set_dists()

    def set_dists(self):
        for dist_name in self.dist_names:
            dist = getattr(scipy.stats, dist_name)
            self.dists[dist_name] = dist

    def plot(self):
        self.plot = self.dists.plot()

        # for i, (dist_name, pdf_fitted) in enumerate(dists.items()):
        # plt.subpl
        # plt.plot(pdf_fitted, label=dist_name)
        # plt.xlim(0,47)
        # plt.legend(loc='upper left')
        # plt.show()


# %%
dists = Distributions(dist_names)
# dists.set_dists()
# dists.dists
# %%

dists.dists


class Fit:
    def __init__(self, distributions):
        self.distributions = distributions

    def fit(self, x, y):
        df_dict = {}
        # print(self.distributions.dists)
        for dist_name, dist in self.distributions.dists.items():
            params = dist.fit(y)
            arg = params[:-2]
            loc = params[-2]
            scale = params[-1]
            print(arg, loc)
            if arg:
                df_dict[dist_name] = dist.pdf(x, *arg, loc=loc, scale=scale) * size
            else:
                df_dict[dist_name] = dist.pdf(x, loc=loc, scale=scale) * size
        print(df_dict)
        self.df = pd.DataFrame.from_dict(df_dict)


F = Fit(distributions)
F.fit
# %%
F.fit(x, y)
# %%
F.df
