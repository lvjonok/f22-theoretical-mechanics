import cv2
import numpy as np

import detect

experiments = list(range(16))


failed = []

for i in [2, 8, 10]:
    print("Experiment", i)
    # get first frame of video using opencv
    cap = cv2.VideoCapture(f'data/{i}/side_roi.MOV')
    ret, frame = cap.read()

    cv2.imwrite(f"images/raw_{i}.jpg", frame)

    try:
        cx, cy = detect.get_yoyo_center(frame)
    except:
        print(f'Experiment {i} failed')

        cv2.imwrite(f'images/{i}_result.jpg', frame)
        failed.append(i)
        continue

    cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)

    cv2.imwrite(f"images/{i}_result.jpg", frame)
    # break

print(f"failed experiments: {failed}")

# # get first frame of video using opencv
# cap = cv2.VideoCapture('data/0/side.MOV')
# ret, frame = cap.read()

# # crop image to x > 340
# frame = frame[:, 340:, :]

# # get center of yoyo
# cx, cy = detect.get_yoyo_center(frame)

# # show frame
# cv2.imshow("Original", frame)
# cv2.waitKey(0)
