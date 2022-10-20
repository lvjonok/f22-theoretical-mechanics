import json
import numpy as np

ticks = np.array([1870, 1801, 1730, 1657, 1585, 1513, 1438, 1366, 1292, 1218, 1146,
                  1075, 1001, 927, 857, 781, 706, 634, 557, 485, 408, 335, 258, 182, 107])

# we have to reverse coordinate system
ticks = 1920 - ticks

cm = np.array([5 * i for i in range(len(ticks))])

# find linear function
a, b = np.polyfit(cm, ticks, 1)
print(a, b)

x_center = 413
x_ticks_cm = (1870 - 1801) / 5

experiment = 0

for experiment in range(1):
    data_path = f"data/{experiment}/side.json"
    pos_path = f"data/{experiment}/posy.json"
    posx_path = f"data/{experiment}/posx.json"

    data = json.load(open(data_path))
    roi = list(map(tuple, data["roi"]))
    print(roi)

    y = np.array([r[1] for r in roi])
    miny, maxy = y.min(), y.max()
    print(miny, maxy)

    pos = np.array(json.load(open(pos_path)))
    pos += miny  # we want to move to default frame 1920x1080 and then convert to cm

    # convert pos to cm
    pos = np.interp(pos, ticks, cm)

    # save pos
    json.dump(pos.tolist(), open(f"data/{experiment}/poscm.json", "w"))

    posx = np.array(json.load(open(posx_path)))
    posx += x_center  # we want to move to default frame 1920x1080 and then convert to cm

    # convert pos to cm
    posx = posx / x_ticks_cm

    # save pos
    json.dump(posx.tolist(), open(f"data/{experiment}/posxcm.json", "w"))

# # plot pos
# import matplotlib.pyplot as plt

# plt.plot(pos)
# plt.xlabel("frame")
# plt.ylabel("cm")

# plt.show()

# # plot ticks for cm

# import matplotlib.pyplot as plt

# plt.plot(cm, ticks, marker='v')

# plt.xlabel("cm")
# plt.ylabel("pixels (y)")

# # draw a line between first and last tick
# plt.plot([cm[0], cm[-1]], [ticks[0], ticks[-1]], color='red')

# plt.show()
