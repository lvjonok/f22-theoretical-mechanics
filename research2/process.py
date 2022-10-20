import json
import matplotlib.pyplot as plt
import cv2
import numpy as np

import detect

experiment = 0
for experiment in range(16):
    print("Experiment", experiment)
    cap = cv2.VideoCapture(f'data/{experiment}/side_roi.MOV')

    # get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        f'data/{experiment}/annotated.mp4', fourcc, fps, (width, height))

    # about 360

    posy = []
    posx = []
    timestamps = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # cv2.imshow("frame", frame)

        # print(f"frame index {cap.get(cv2.CAP_PROP_POS_FRAMES)}")
        frameidx = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        k = cv2.waitKey(1)
        if k == ord('s'):
            cv2.imwrite(f"data/{experiment}/test_{frameidx}.jpg", frame)
        # cv2.waitKey(0)

        try:
            cx, cy = detect.get_yoyo_center(frame)

            # draw circle
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

            posy.append(cy)
            posx.append(cx)

            # get current timestamp
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            timestamps.append(timestamp)
        except:
            # print(f'Experiment {experiment} failed')
            posy.append(None)
            continue

        # cv2.imshow("annotated", frame)
        out.write(frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()

    # save out video
    out.release()

    # find missed values
    missed = sum(1 for x in posy if x is None)

    print(f"missed {missed} values out of {len(posy)}")

    posy = [x if x else -1 for x in posy]

    # drop last values if they are 0 for timestamp
    while timestamps[-1] == 0:
        timestamps.pop()
        posy.pop()
        posx.pop()

    # save posy to file
    with open(f"data/{experiment}/posy.json", "w") as f:
        json.dump(posy, f)

    # save posx to file
    with open(f"data/{experiment}/posx.json", "w") as f:
        json.dump(posx, f)

    with open(f"data/{experiment}/time.json", "w") as f:
        json.dump(timestamps, f)

    # erase plot
    plt.clf()

    # plot posy
    plt.plot(timestamps, posy)

    plt.savefig(f"data/{experiment}/posy.png")

    # erase plot
    plt.clf()

    # plot posx
    plt.plot(timestamps, posx)

    plt.savefig(f"data/{experiment}/posx.png")
