import numpy as np
from matplotlib import pyplot as plt

from simulation import headless_simulations


def plot_histogram(frequencies, title):
    # TODO frequency should be from 0 to 1?
    fig, ax = plt.subplots(1, 1)

    # create 5 bins from 0 to 1
    bins = np.linspace(0, 1, 6)

    ax.hist(frequencies, bins)
    ax.set_xticks(bins)
    ax.set_xlabel('Proportion going right')
    ax.set_ylabel('Frequency')
    ax.set_title(title)


def run_experiments_1_1(shoals=30):
    # group size 2
    replicas_top = 1
    replicas_bottom = 1

    frequencies = headless_simulations(shoals, fishes=2, replicas_top=replicas_top,
                                       replicas_bottom=replicas_bottom)

    plot_histogram(frequencies, '1:1 group size 2')
