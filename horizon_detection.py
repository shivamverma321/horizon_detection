import cv2
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from utils import detect_horizon_line


# grab images from folder
images = []
for file in os.listdir(os.getcwd() + "/images"):
    if file.endswith(".png"):
        images.append(cv2.imread(os.getcwd() + "/images/" + file, 0))


num_sliding_windows = 16
delta = int(2448 / num_sliding_windows)
top_crop = 750
bottom_crop = 1400
cnt = 1
for img in images:
    # crop the image so that it does not include too much of the top or bottom_crop
    # this is useful as there could be bright sunglight that throws the algorithm off
    img_crop = img[top_crop : bottom_crop, :]

    # Then we run a sliding window and compute the horizon points just in that small window
    points = []
    for j in range(num_sliding_windows):
        temp_img = img_crop[:, j * delta : (j + 1) * delta]
        # compute the horizon points at these windows
        horizon_x1, horizon_x2, horizon_y1, horizon_y2 = detect_horizon_line(temp_img)
        if(horizon_y1 != -1):
            points.append((horizon_y1, horizon_x1 + j * delta))
        if(horizon_y2 != -1):
            points.append((horizon_y2, horizon_x2 + j * delta))


    points.sort()
    # Some points may be not in line with the other points so we drop outliers
    points = points[:int(len(points)*(0.75))]

    # plot the points
    for x, y in points:
        img = cv2.circle(img, (y,x + top_crop), radius=15, color=(255, 255, 255), thickness=-1)
    # save results 
    cv2.imwrite(os.getcwd() + "/results/" + "{}.png".format(cnt), img)
    cnt += 1
