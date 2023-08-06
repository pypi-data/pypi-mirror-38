import numpy as np
from fractions import Fraction
from statistics import mean, pstdev

restricted_data = []
for i in range(0, 20):
    minint = np.random.choice(np.arange(-5, 0))
    maxint = np.random.choice(np.arange(20, 100))
    npart = np.random.choice(np.arange(20, 50))
    scale = np.arange(minint, maxint, 1)
    restrict = np.random.choice([1, 2, 3, 4], size=10)
    restricted_scale = [i for i in scale if i not in restrict]
    data = np.random.choice(restricted_scale, size=npart)
    restrict_dict = {k:v for k, v in zip(*np.unique(restrict, return_counts=True))}
    data = np.concatenate([data, restrict])
    m = np.round(data.mean(), 2)
    sd = np.round(data.std(ddof=1), 2)
    n = len(data)
    restricted_data.append([n, m, sd, 2, 2, minint, maxint, restrict_dict])
print(restricted_data)


single_restricted_data = []
for i in range(0, 20):
    minint = 0
    maxint = np.random.choice(np.arange(5, 10))
    npart = np.random.choice(np.arange(20, 50))
    scale = np.arange(minint, maxint, 1)
    restricts = np.random.choice(scale[1:-1], 2)
    restricted_scale = [i for i in scale if i not in restricts]
    data = np.random.choice(restricted_scale, size=npart)
    restrict_dict = {r:0 for r in restricts}
    m = np.round(data.mean(), 2)
    sd = np.round(data.std(ddof=1), 2)
    n = len(data)
    single_restricted_data.append([n, m, sd, 2, 2, minint, maxint, restrict_dict])
print(single_restricted_data)

two_items_data = []
for i in range(0, 20):
    minint = 0
    maxint = np.random.choice(np.arange(5, 10))
    npart = np.random.choice(np.arange(20, 50))
    scale = np.arange(minint, maxint+0.4, 0.5)
    data = np.random.choice(scale, size=npart)
    m = np.round(data.mean(), 2)
    sd = np.round(data.std(ddof=1), 2)
    two_items_data.append([npart, m, sd, 2, 2, minint, maxint, 2])
print(two_items_data)

three_items_data = []
for i in range(0, 20):
    minint = 0
    maxint = np.random.choice(np.arange(5, 10))
    npart = np.random.choice(np.arange(20, 50))
    scale = np.arange(minint, maxint, Fraction(1, 3))
    data = np.random.choice(scale, size=npart)
    m = float(round(mean(data), 2))
    sd = float(round(pstdev(data), 2))
    three_items_data.append([npart, m, sd, 2, 2, minint, maxint, 3])
print(three_items_data)