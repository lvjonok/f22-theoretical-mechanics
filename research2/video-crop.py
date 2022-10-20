import json
import os
import cv2
import numpy as np

for experiment in range(16):
    cap = cv2.VideoCapture(f'data/{experiment}/side.MOV')
    info = json.load(open(f'data/{experiment}/side.json'))

    start = info['start_frame']
    finish = info['end_frame']

    cmd = f"ffmpeg -i data/{experiment}/side.MOV -ss {start / 240} -c:v libx264 -frames:v {finish - start} data/{experiment}/side_crop.mp4"

    # execute cmd
    os.system(cmd)

    print(f'Experiment {experiment} done')

