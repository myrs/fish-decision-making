import time
import numpy as np
from matplotlib import pyplot as plt

from simulation import headless_simulations
from plots import plot_histogram
from experimental_setups import SETUPS


def run_experiment(shoals=30, fishes=2, replicas_top=0, replicas_bottom=0, follow_refugia_force=0.2):
    frequencies = headless_simulations(shoals, fishes=fishes,
                                       replicas_top=replicas_top,
                                       replicas_bottom=replicas_bottom,
                                       follow_refugia_force=follow_refugia_force)

    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    plot_histogram(ax,
                   frequencies,
                   f'{replicas_bottom}: {replicas_top}, group size {fishes}')
    fig.show()
    return frequencies


def run_experiments(shoals=30, replicas_top=0, replicas_bottom=0, follow_refugia_force=0.2):
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
                                           replicas_bottom=replicas_bottom,
                                           follow_refugia_force=follow_refugia_force)

        all_frequencies.append(frequencies)

    print('all frequencies:', all_frequencies)

    return all_frequencies


def run_set(shoals=30, follow_refugia_force=0.2):
    start = time.time()

    results = []
    for setup in SETUPS:
        r = run_experiments(shoals=shoals, replicas_bottom=setup[0], replicas_top=setup[1], 
            follow_refugia_force=follow_refugia_force)
        results.append(r)

    end = time.time()
    print(f'\n all sets time: {end - start:.2f}')

    return results
