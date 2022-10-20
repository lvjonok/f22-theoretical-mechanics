import cv2
import numpy as np

experiment = 0

# # we will store y each 5cm and then interpolate function
# ticks = []


# def click_show(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print(x, y)
#         # draw horizontal line
#         cv2.line(frame, (0, y), (frame.shape[1], y), (0, 0, 255), 1)
#         cv2.imshow("frame", frame)

#         ticks.append(y)


# # read first frame of video
# cap = cv2.VideoCapture(f'data/{experiment}/side.MOV')
# ret, frame = cap.read()

# cv2.imshow('frame', frame)
# cv2.setMouseCallback("frame", click_show)

# cv2.waitKey(0)

# print(ticks)

ticks = [1870, 1801, 1730, 1657, 1585, 1513, 1438, 1366, 1292, 1218, 1146, 1075, 1001, 927, 857, 781, 706, 634, 557, 485, 408, 335, 258, 182, 107]
cm = [5 * i for i in range(len(ticks))]

# plot ticks for cm

import matplotlib.pyplot as plt 

plt.plot(cm, ticks, marker='v')
plt.xlabel("cm")
plt.ylabel("pixels (y)")

# draw a line between first and last tick
plt.plot([cm[0], cm[-1]], [ticks[0], ticks[-1]], color='red', label="pixels vs cm correspondence")

plt.legend()
plt.show()