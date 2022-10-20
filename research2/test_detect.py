import fnmatch
import os

import cv2
import detect


experiment = 1

files = []
# get filenames in pattern test_*.jpg
for file in os.listdir(f"data/{experiment}"):
    if fnmatch.fnmatch(file, "test_*.jpg"):
        files.append(file)

# sort files by number
files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

for fname in files:
    print(fname)
    # open cv2 image
    frame = cv2.imread(f"data/{experiment}/{fname}")

    try:
        cx, cy = detect.get_yoyo_center(frame)

        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
    except:
        print(f"failed {fname}")
        # continue

    cv2.imshow("frame", frame)
    # break

    # wait until q is pressed
    while True:
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
