import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

datas = []

for experiment in range(16):
    data = json.load(open(f"data/{experiment}/side.json"))

    datas.append(data)


# create dataframe from list of dicts
df = pd.DataFrame(datas)

# create a new column with experiments from index
df['experiments'] = df.index


# aggregate data by l, join indices
df = df.groupby('l').agg({'experiments': lambda x: list(x)})

# iterate through l values
for l, experiments in df.iterrows():
    print(l, experiments)
    # plot experiments
    plt.clf()

    plt.title(f"Rope length {l} cm")

    for experiment in experiments['experiments']:
        print(experiment)
        # load data for experiment 0
        posy = np.array(json.load(open(f"data/{experiment}/poscm.json")))
        time = np.array(json.load(open(f"data/{experiment}/time.json")))

        posy = posy[: len(time)]

        plt.xlabel("Time (s)")
        plt.ylabel("Position (cm)")

        # plot posy
        plt.plot(time, posy, label=f"Experiment {experiment}")

    plt.legend()
    plt.savefig(f"reportimages/raw_{l}.png")
