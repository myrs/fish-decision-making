import time
import numpy as np
from matplotlib import pyplot as plt

from simulation import headless_simulations


def plot_histogram(ax, frequencies, title, bins_n=6):
    # TODO frequency should be from 0 to 1?

    # create 5 bins from 0 to 1
    bins = np.linspace(0, 1, bins_n)

    # calculate weight so all histograms would sum to 1
    weights = np.ones_like(frequencies) / len(frequencies)

    ax.hist(frequencies, bins, weights=weights)
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
                   f'{replicas_top}: {replicas_bottom}, group size {fishes}')
    fig.show()
    return frequencies


def run_experiments(shoals=30, replicas_top=0, replicas_bottom=0):
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

    fig, ax = plt.subplots(1, 3, constrained_layout=True)

    # plotting histogram apart as it seams to consume memory and crash
    for i in range(len(group_sizes)):
        plot_histogram(ax[i],
                       all_frequencies[i],
                       f'{replicas_top}:{replicas_bottom}, group size {group_sizes[i]}')

    fig.show()

    print('all frequencies:', all_frequencies)

    return all_frequencies

def run_set(shoals=30):
    start = time.time()

    results = []
    # 1:1 - 1 bottom, 1 top
    r = run_experiments(shoals=shoals, replicas_bottom=1, replicas_top=1)
    results.append(r)

    # 2:2 - 2 bottom, 2 top
    r = run_experiments(shoals=shoals, replicas_bottom=2, replicas_top=2)
    results.append(r)
    
    # 0:1 - 0 bottom, 1 top
    r = run_experiments(shoals=shoals, replicas_bottom=0, replicas_top=1)
    results.append(r)

    # 0:2 - 0 bottom, 2 top 
    r = run_experiments(shoals=shoals, replicas_bottom=-0, replicas_top=2)
    results.append(r)
    
    # 0:3 - 0 bottom, 3 top
    r = run_experiments(shoals=shoals, replicas_bottom=0, replicas_top=3)
    results.append(r)
    
    # 1:2 - 1 bottom, 2 top
    r = run_experiments(shoals=shoals, replicas_bottom=1, replicas_top=2)
    results.append(r)
    
    # 1:3 - 1 bottom, 2 top
    r = run_experiments(shoals=shoals, replicas_bottom=1, replicas_top=2)
    results.append(r)

    end = time.time()
    print(f'\n all sets time: {end - start:.2f}')

    return results
