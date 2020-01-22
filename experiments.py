import time
import numpy as np
from matplotlib import pyplot as plt

from simulation import headless_simulations

# global for experiment setups
SETUPS = [
    # 1:1 - 1 left (bottom), 1 top (right)
    (1, 1),

    # 2:2 - 2 left (bottom), 2 top (right)
    (2, 2),

    # 0:1 - 0 left (bottom), 1 top (right)
    (0, 1),

    # 0:2 - 0 left (bottom), 2 top  (right)
    (0, 2),

    # 0:3 - 0 left (bottom), 3 top (right)
    (0, 3),

    # 1:2 - 1 left (bottom), 2 top (right)
    (1, 2),

    # 1:3 - 1 left (bottom), 3 top (right)
    (1, 3)
]


def plot_histogram(ax, frequencies, title, bins_n=6, original_frequencies=None):
    # TODO frequency should be from 0 to 1?

    # create 5 bins from 0 to 1
    bins = np.linspace(0, 1, bins_n)

    # if original_frequencies:
    #     weights_original = np.ones_like(original_frequencies) / len(original_frequencies)
    #     ax.hist(original_frequencies, bins, weights=weights_original,
    #             color='gray', alpha=0.5)

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


def run_experiment(shoals=30, fishes=2, replicas_top=0, replicas_bottom=0):
    frequencies = headless_simulations(shoals, fishes=fishes,
                                       replicas_top=replicas_top,
                                       replicas_bottom=replicas_bottom)

    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    plot_histogram(ax,
                   frequencies,
                   f'{replicas_bottom}: {replicas_top}, group size {fishes}')
    fig.show()
    return frequencies


def run_experiments(shoals=30, replicas_top=0, replicas_bottom=0, original_frequencies=None):
    """ 
    run %shoals experiments 
    for given number %replicas_top and %replicas_bottom
    for shoal sizes 2, 4 and 8
    """
    all_frequencies = []

    group_sizes = [2, 4, 8]
    for i, group_size in enumerate(group_sizes):
        print(f'\n\n======== Simulation for {i + 1} of {len(group_sizes)}\n' +
              f'Group size: {group_size}, ' +
              f'replicas top: {replicas_top},' +
              f'replicas bottom: {replicas_bottom}')

        frequencies = headless_simulations(shoals, fishes=group_size,
                                           replicas_top=replicas_top,
                                           replicas_bottom=replicas_bottom)

        all_frequencies.append(frequencies)

    print('all frequencies:', all_frequencies)

    return all_frequencies


def run_set(shoals=30):
    start = time.time()

    results = []
    for setup in SETUPS:
        r = run_experiments(shoals=shoals, replicas_bottom=setup[0], replicas_top=setup[1])
        results.append(r)

    end = time.time()
    print(f'\n all sets time: {end - start:.2f}')

    return results
