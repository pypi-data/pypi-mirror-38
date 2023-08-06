import numpy as np
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