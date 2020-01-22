import numpy as np
import scipy.stats

def generate_random_distribution(top=1, bottom=1):
    distribution = []    
    probability = top / (top + bottom)

    for i in range(30):
        top = 0
        for i in range(8):
            if probability > np.random.random():
                top += 1
        proportion = top / 8
    
        distribution.append(proportion)
    
    return distribution




