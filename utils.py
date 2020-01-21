from scipy.stats import truncnorm

def random_trunc(mean=0, sd=1, low=0, upp=20):
    x = get_truncated_normal(mean=mean, sd=sd, low=low, upp=upp)
    return x.rvs()

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)