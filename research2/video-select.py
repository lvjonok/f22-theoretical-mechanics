import json

lengths = {}

for experiment in range(16):
    data = json.load(open(f"data/{experiment}/side.json"))

    inlength = data['l']

    try:
        lengths[inlength].append(experiment)
    except KeyError:
        lengths[inlength] = [experiment]


print(lengths)
