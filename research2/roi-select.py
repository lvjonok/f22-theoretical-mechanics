import json
import cv2
import numpy as np

experiment = 15

video_path = f"data/{experiment}/side_crop.mp4"
data_path = f"data/{experiment}/side.json"

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        # draw a rectangle around the region of interest
        # cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        # cv2.imshow("frame", image)


cap = cv2.VideoCapture(video_path)

cv2.namedWindow("frame")
cv2.setMouseCallback('frame', click_and_crop)

while (cap.isOpened()):
    ret, image = cap.read()
    if ret == True:
        # draw rectangle if we have enough points
        if len(refPt) > 1:
            cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)

        cv2.imshow('frame', image)
        print(ret, cap.get(cv2.CAP_PROP_POS_FRAMES), image.shape)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('r'):
            # save coordinates and allow new roi to be made
            break
        elif k == ord(' '):
            cv2.waitKey(0)
    else:
        break

# save changes to roi definition file
if (len(refPt) > 1):
    data = {}
    with open(data_path, 'r') as f:
        data = json.load(f)
    with open(data_path, 'w') as f:
        data['roi'] = refPt
        json.dump(data, f)
