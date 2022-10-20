import json
import os
import cv2
import numpy as np

for experiment in [13]:
    print(f"Start experiment {experiment}")
    cap = cv2.VideoCapture(f'data/{experiment}/side.MOV')
    info = json.load(open(f'data/{experiment}/side.json'))

    start = info['start_frame']
    finish = info['end_frame']

    # get fps info
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("fps of video is {}".format(fps))

    cmd = f"ffmpeg -hide_banner -loglevel error -i data/{experiment}/side.MOV" \
        + f" -ss {start/fps:.0f} -t {(finish - start)/fps:.0f} data/{experiment}/side_cropped.MOV"

    # cmd = f"ffmpeg -i data/{experiment}/side.MOV -ss {start / 240 + 0.4} -c:v libx264 -frames:v {finish - start} data/{experiment}/side_crop.mp4"

    # execute cmd
    os.system(cmd)

    print(f'Experiment {experiment} done')
