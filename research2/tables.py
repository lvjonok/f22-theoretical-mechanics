import json
import numpy as np
import pandas as pd

datas = []

for experiment in range(16):
    data = json.load(open(f"data/{experiment}/side.json"))

    datas.append(data)

# create dataframe from list of dicts
df = pd.DataFrame(datas).loc[:, ['l', 'oscillations', 'max-stretch']]

# group by l and join oscillations
df = df.groupby('l').agg(
    {'oscillations': lambda x: list(x), 'max-stretch': lambda x: list(x)})

# add mean and std columns
df['osc-mean'] = df['oscillations'].apply(np.mean)
df['osc-std'] = df['oscillations'].apply(np.std)

df['stretch-mean'] = df['max-stretch'].apply(np.mean)
df['stretch-std'] = df['max-stretch'].apply(np.std)

# df is 1st table from assignment

print(df.loc[:, ['oscillations', 'osc-mean', 'osc-std']].head().to_markdown())

print(df.loc[:, ['max-stretch', 'stretch-mean',
      'stretch-std']].head().to_markdown())
