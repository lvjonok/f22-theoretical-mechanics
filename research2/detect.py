from typing import Tuple
import cv2
import numpy as np


def get_yoyo_center(frame, prev=(0, 0)):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # something around 34 160 186
    # create hsv filter for (34, 160, 186)
    lower_yoyo = np.array([0, 5, 0])
    upper_yoyo = np.array([179, 255, 130]) # till 110
    # works for black very good

    # create mask
    mask = cv2.inRange(hsv, lower_yoyo, upper_yoyo)

    # create hsv filter for yellow
    lower_yellow = np.array([0, 70, 0])
    upper_yellow = np.array([179, 255, 255])

    # create mask for yellow
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # show mask
    # cv2.imshow("mask", mask)
    # cv2.imshow("mask_yellow", mask_yellow)

    # merge two masks
    mask = cv2.bitwise_or(mask, mask_yellow)

    # find contours in the mask and display them
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # get areas of contours
    contours = [c for c in contours if cv2.contourArea(c) > 100]
    areas = [cv2.contourArea(c) for c in contours]

    # print(f"there are {len(areas)} raw contours")
    # print(areas)

    # filter only contours with area > 1000 and < 3000
    contours = [c for c in contours if 1000 < cv2.contourArea(c)]
    areas = [cv2.contourArea(c) for c in contours]

    cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)

    # print("Number of contours:", len(contours))
    # print("Areas of contours:", areas)

    # sort contours by area
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # def get_middle(contour) -> Tuple[float, float]:
    #     # get center of contour
    #     M = cv2.moments(contour)
    #     cx = int(M["m10"] / M["m00"])
    #     cy = int(M["m01"] / M["m00"])
    #     return cx, cy

    # def get_distance(a, b):
    #     return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

    # # find contour which middle is the closest to the previous middle
    # # if there is no previous middle, use the first contour
    # if prev == (0, 0):
    #     contour = contours[0]
    # else:
    #     # get middle of all contours
    #     middles = [get_middle(c) for c in contours]

    #     # get distance of middles to previous middle
    #     distances = [get_distance(m, prev) for m in middles]

    #     # get index of smallest distance
    #     index = distances.index(min(distances))

    #     # get contour with smallest distance
    #     contour = contours[index]

    # # get middle of contour
    # cx, cy = get_middle(contour)

    # return cx, cy

    cx, cy = 0, 0

    # get middle of each contour
    for c in contours[:1]:
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        # print("Center:", cx, cy)
        # cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
        return cx, cy

    raise Exception("No yoyo found")
    return cx, cy
