import numpy as np
import scipy.stats

def generate_random_distribution(top=1, bottom=1, fishes=2):
    distribution = []    
    probability = top / (top + bottom)

    for i in range(30):
        top = 0
        
        for i in range(fishes):
            if probability > np.random.random():
                top += 1
        
        proportion = top / fishes
    
        distribution.append(proportion)
    
    return distribution

def test_significance(d1, d2):
    _, p = scipy.stats.ks_2samp(d1, d2)
    
    return verbose_significance(p)

def verbose_significance(p):
    if p > 0.1:
        return 'ns'
    elif p > 0.05:
        return '*'
    elif p > 0.01:
        return '**'
    else:
        return '***'

def distribution_significance(dist, fishes):
    """ 
    distribution significance for rejecting two null-hypothesis:
    1. fishes move random
    2. fished follow replica in proportion
    """
    ps = []
    for i in range(15):
        swim_random_dist = generate_random_distribution(1, 1, fishes)
        _, p = scipy.stats.ks_2samp(dist, swim_random_dist)
        ps.append(p)

    p_mean = np.mean(ps)

    return verbose_significance(p_mean)

def distribution_significance_old(dist, top, bottom, fishes):
    """ 
    distribution significance for rejecting two null-hypothesis:
    1. fishes move random
    2. fished follow replica in proportion
    """
    swim_random_dist = generate_random_distribution(1, 1, fishes)
    follow_replica_dist = generate_random_distribution(top, bottom, fishes)

    significance_random = test_significance(dist, swim_random_dist)
    significance_follow_replica = test_significance(dist, follow_replica_dist)

    return significance_random, significance_follow_replica





