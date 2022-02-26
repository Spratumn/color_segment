
import os
import time
import cv2
import numpy as np
from tqdm import tqdm
from utils import *


def color_segment_1(image, min_size=20):
    image = vote_filter2d(image, ksize=5)
    image_clean = clean_background(np.array(image), min_size=min_size)

    image_clean = cv2.GaussianBlur(image_clean, (5, 5), 1)
    gray = cv2.cvtColor(image_clean, cv2.COLOR_BGR2GRAY)
    rects = get_rects_from_gray_image(gray, min_size=min_size)
    return rects


def color_segment_2(image, min_size=20, min_area=400):
    image = vote_filter2d(image, ksize=5)
    image_clean = clean_background(np.array(image), min_size=min_size)

    colors, masks = get_sub_masks(image_clean, min_area=min_area)
    masks = merge_masks(colors, masks)
    masks = filter_edge_mask(masks)

    rects = []
    for mask in masks:
        rects += get_rects_from_mask(mask, min_size=20)
    return rects


def save_result_to_txt(file_path, rects, left_top, bottom_right, width, height):

    ppx = width / (bottom_right[0] - left_top[0])
    ppy = height / (bottom_right[1] - left_top[1])
    with open(file_path, 'w') as f:
        for (x1, y1, x2, y2) in rects:
            x1 = round(x1 * ppx, 3)
            y1 = round(y1 * ppy, 3)
            x2 = round(x2 * ppx, 3)
            y2 = round(y2 * ppy, 3)
        f.write(f'{x1},{y1},{x2},{y2}\n')



if __name__ == '__main__':
    source_dir = 'images'
    result_dir = 'results-2'

    image_names = os.listdir(source_dir)
    start_all = time.time()
    for image_name in tqdm(image_names[:20]):
        if not image_name.endswith(('.png', '.jpg', '.jpeg')):continue
        image_path = os.path.join(source_dir, image_name)
        image = cv2.imread(image_path)
        
        # color_rects = color_segment_1(image)
        color_rects = color_segment_2(image)

        color_rects = nms(color_rects, iou_thresh=0.7)

        for (x1, y1, x2, y2) in color_rects:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.imwrite(os.path.join(result_dir, image_name), image)

    print(f'mean time: {(time.time() - start_all) / 20}')
