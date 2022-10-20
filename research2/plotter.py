import matplotlib.pyplot as plt

import numpy as np

import json

experiment = 0

for experiment in range(1):
    pos_path = f"data/{experiment}/poscm.json"
    posx_path = f"data/{experiment}/posxcm.json"

    pos = np.array(json.load(open(pos_path)))
    posx = np.array(json.load(open(posx_path)))

    # plot pos
    plt.plot(posx)

    plt.show()