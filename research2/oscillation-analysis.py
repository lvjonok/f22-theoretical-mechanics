import matplotlib.pyplot as plt
import json
import numpy as np

experiment = 0

for experiment in range(16):
    # Load the data
    pos = np.array(json.load(open(f"data/{experiment}/poscm.json")))

    # apply median filter for data with some window
    rawpos = pos.copy()
    window = 70
    pos = np.convolve(pos, np.ones((window,))/window, mode='same')

    # find extremas
    extrema = np.diff(np.sign(np.diff(pos))).nonzero()[0] + 1  # local min+max

    # filter only local maxima
    maxima = (pos[extrema] > pos[extrema + 20]
              ) & (pos[extrema] > pos[extrema - 20])

    minima = (pos[extrema] < pos[extrema + 20]
              ) & (pos[extrema] < pos[extrema - 20])

    # find indices of minima and maximas
    maxima_x = extrema[maxima]
    minima_x = extrema[minima]

    true_maximas = []

    for max in maxima_x:
        try:
            prev_min = minima_x[minima_x < max][-1]
        except:
            prev_min = 0

        try:
            next_min = minima_x[minima_x > max][0]
        except:
            next_min = 1000

        valprev = pos[prev_min]
        valnext = pos[next_min]
        valmax = pos[max]

        peakup = valmax - valprev
        peakdown = valmax - valnext
        # print(f"max: {valmax}, prev: {valprev}, next: {valnext}")
        # print(f"peak up {peakup}, peak down {peakdown}")

        # filter maximas only where peakup and peakdown were greater than 2
        if peakup > 2 and peakdown > 2:
            true_maximas.append(max)

    peaks = []

    # Plot the data
    plt.plot(rawpos)

    # Plot the extrema
    # plt.plot(extrema, pos[extrema], "x")

    # plot maxima
    plt.plot(extrema[maxima], rawpos[extrema[maxima]], "o", color='red')

    # plot minima
    plt.plot(extrema[minima], rawpos[extrema[minima]], "x", color='red')

    # plot true maximas
    plt.plot(true_maximas, rawpos[true_maximas], "o", color='green')

    print(
        f"experiment {experiment} there are {len(true_maximas)} oscillations")

    plt.show()

    data = {}
    # load data from file
    with open(f"data/{experiment}/side.json") as f:
        data = json.load(f)

    data['oscillations'] = len(true_maximas)

    data['max-stretch'] = rawpos[minima_x[1]]
    # round number to 3 decimal places
    data['max-stretch'] = round(data['max-stretch'], 3)

    print(f"max stretch was {data['max-stretch']}")

    # write data to file
    with open(f"data/{experiment}/side.json", 'w') as f:
        json.dump(data, f)
