'''
Test speed
'''

import numpy as np
import sciris as sc
import covasim as cv

max_n   = int(1e6)
n       = int(1e2)
repeats = int(1e5)


with sc.timer('Numpy'):
    for r in range(repeats):
        np.random.choice(max_n, n, replace=True)

with sc.timer('Numba'):
    for r in range(repeats):
        cv.choose_r(max_n, n)
