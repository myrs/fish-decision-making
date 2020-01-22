import numpy as np
from matplotlib import pyplot as plt
from experiments import SETUPS


def plot_histogram(ax, frequencies, title, bins_n=6, original_frequencies=None):
    # create 5 bins from 0 to 1
    bins = np.linspace(0, 1, bins_n)

    # calculate weight so all histograms would sum to 1
    weights = np.ones_like(frequencies) / len(frequencies)
    # ax.hist(frequencies, bins, weights=weights, rwidth=0.8)
    ax.hist(frequencies, bins, weights=weights, rwidth=0.8)

    if original_frequencies:
        weights_original = np.ones_like(original_frequencies) / len(original_frequencies)
        ax.hist(original_frequencies, bins, weights=weights_original,
                color='silver', alpha=0.8, rwidth=0.4)

    ax.set_xticks(bins)
    ax.set_ylim((0, 1))
    ax.set_xlabel('Proportion going right')
    ax.set_ylabel('Frequency')
    ax.set_title(title)


def plot_histogram_for_setup(replicas_bottom, replicas_top, setup_frequencies_data,
                             original_frequencies_data, group_sizes=[2, 4, 8]):
    """ plot histogram for one setup """
    fig, ax = plt.subplots(1, 3, constrained_layout=True)

    # plotting histogram apart as it seams to consume memory and crash
    for i, group_size in group_sizes:
        plot_histogram(ax[i],
                       setup_frequencies_data[i],
                       f'{replicas_bottom}:{replicas_top}, group size {group_size}',
                       original_frequencies=original_frequencies_data[i])

    fig.show()

def plot_histograms_for_set(experiments_data, original_data):
    """ plot all the histograms for each setup"""
    for i, setup in enumerate(SETUPS):
        plot_histogram_for_setup(setup[0], setup[1], experiments_data[i], original_data[i])
