
import json
import os


for experiment in [13]:
    print(f"Doint experiment {experiment}")
    data_path = f"data/{experiment}/side.json"
    video_path = f"data/{experiment}/side_cropped.MOV"
    new_video_path = f"data/{experiment}/side_roi.MOV"

    data = json.load(open(data_path))

    roi = list(map(tuple, data["roi"]))

    xs, ys = [r[0] for r in roi], [r[1] for r in roi]
    xs.sort()
    ys.sort()

    print(roi)
    print(xs, ys)

    x, y, out_w, out_h = xs[0], ys[0], xs[-1] - xs[0], ys[-1] - ys[0]

    cmd = f"ffmpeg -hide_banner -loglevel error -i {video_path} -vf crop={out_w}:{out_h}:{x}:{y} -c:a copy {new_video_path}"

    os.system(cmd)
