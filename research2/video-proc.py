import json
import cv2
import numpy as np

experiment = 15

cap = cv2.VideoCapture(f'data/{experiment}/side.MOV')
out_path = f'data/{experiment}/side.json'

start = 0
finish = 0

# play video
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('frame', frame)

        # show which frame is being processed in gui
        cv2.putText(frame, str(cap.get(cv2.CAP_PROP_POS_FRAMES)),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        print(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # press space to pause
        k = cv2.waitKey(1) & 0xFF
        if k in list(map(ord, [' ', 'q', 's', 'f'])):
            if k == ord('q'):
                break
            if k == ord('s'):
                print("start is at frame {}".format(
                    cap.get(cv2.CAP_PROP_POS_FRAMES)))
                start = cap.get(cv2.CAP_PROP_POS_FRAMES)
            if k == ord('f'):
                print("finish is at frame {}".format(
                    cap.get(cv2.CAP_PROP_POS_FRAMES)))
                finish = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cv2.waitKey(0)

    else:
        break

# save start and finish frame to json file
with open(out_path, 'w') as f:
    res = {
        "start_frame": start,
        "end_frame": finish
    }
    json.dump(res, f)
