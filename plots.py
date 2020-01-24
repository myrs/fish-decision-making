import numpy as np
from matplotlib import pyplot as plt
from experimental_setups import SETUPS
from hypothesis_testing import distribution_significance


def plot_histogram(ax, frequencies, title, bins_n=6, original_frequencies=None):
    # create 5 bins from 0 to 1
    bins = np.linspace(0, 1, bins_n)

    # calculate weight so all histograms would sum to 1
    weights = np.ones_like(frequencies) / len(frequencies)
    # ax.hist(frequencies, bins, weights=weights, rwidth=0.8)
    ax.hist(frequencies, bins, weights=weights, rwidth=0.8)

    if type(original_frequencies) == np.ndarray and original_frequencies[0] is not None:
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
    for i, group_size in enumerate(group_sizes):
        plot_histogram(ax[i],
                       setup_frequencies_data[i],
                       f'{replicas_bottom}:{replicas_top}, group size {group_size}',
                       original_frequencies=original_frequencies_data[i])

    fig.show()


def plot_histograms_for_set(experiments_data, original_data):
    """ plot all the histograms for each setup"""
    for i, setup in enumerate(SETUPS):
        plot_histogram_for_setup(setup[0], setup[1], experiments_data[
                                 i], original_data[i])


def group_plot(group_data, group_size):
    fig, ax = plt.subplots(1, 1, constrained_layout=True)

    rows = group_data.shape[0]
    # calculate mean by row (sum columns or each row)
    # = get mean data for each setup (e.g. top 1, bottom 1)
    mean = np.mean(group_data, axis=1)
    std = np.std(group_data, axis=1)

    ax.scatter(range(rows), mean, color='royalblue')

    ax.errorbar(range(rows), mean, yerr=std,
                fmt='none', lw=1.2, elinewidth=1.4, capsize=2, markeredgewidth=1.4,
                color='royalblue')

    max_y = -np.inf
    min_y = np.inf
    for i in range(rows):
        bottom, top = SETUPS[i]
        significance = distribution_significance(group_data[i], group_size)
        # height = rectangle.get_height()
        x = i
        y = mean[i] + std[i] + 0.01
        bottom = mean[i] - std[i] - 0.01
        max_y = y if y > max_y else max_y
        min_y = bottom if bottom < min_y else min_y

        # up - random null hypothesis rejection significance 
        plt.text(x, y + 0.05, significance, ha='center', va='bottom')
        # down - follow the replica in proportion hypothesis rejection significance
        # plt.text(x, y, sign_follow, ha='center', va='bottom')

    xticks = [f'{s[0]}:{s[1]}' for s in SETUPS]
    print(xticks)

    ax.set_xticklabels([''] + xticks)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xlabel('Replicas going left:right')
    ax.set_ylabel('Proportion going right')

    ax.set_ylim((0, max_y + 0.15))

    ax.set_title(f'Group size {group_size}')

    fig.show()


def groups_plots(experiments_data, group_sizes=[2, 4, 8]):
    for i, group_size in enumerate(group_sizes):
        group_plot(experiments_data[:, i], group_size)
