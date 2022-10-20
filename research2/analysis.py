import json
from matplotlib import pyplot as plt
import numpy as np

# plot images in grid 5x3
fig, axs = plt.subplots(5, 3, figsize=(15, 15))

# loop through all images
for i in range(15):
    # read pos
    pos = np.array(json.load(open(f"data/{i}/poscm.json")))

    # plot pos
    axs[i // 3, i % 3].plot(pos)
    axs[i // 3, i % 3].set_title(f"Experiment {i}")

    # # read image
    # img = plt.imread(f'data/{i}/position.png')

    # # get row and column
    # row = i // 3
    # col = i % 3

    # print(f"row {row}, col {col}")

    # # # filter image y > 1000
    # # img = img[1200:, :, :]

    # # plot image
    # axs[row, col].imshow(img)
    # # axs[row, col].set_title(f'Experiment {i}')
    # axs[row, col].set_xticks([])
    # axs[row, col].set_yticks([])
    # axs[row, col].set_aspect('equal')


plt.subplots_adjust(wspace=0, hspace=0)

plt.show()
