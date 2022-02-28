
import os
import cv2
import ast
import numpy as np
from utils import *

# 速度快，但效果不太好
def color_segment_1(image, min_size=20):
    image = vote_filter2d(image, ksize=5)
    image_clean = clean_background(np.array(image), min_size=min_size)

    image_clean = cv2.GaussianBlur(image_clean, (5, 5), 1)
    gray = cv2.cvtColor(image_clean, cv2.COLOR_BGR2GRAY)
    rects, areas = get_rects_from_gray_image(gray, min_size=min_size)
    return rects, areas

# 效果好，速度较慢
def color_segment_2(image, min_size=20, min_area=400):
    image = vote_filter2d(image, ksize=5)
    image_clean = clean_background(np.array(image), min_size=min_size)

    colors, masks = get_sub_masks(image_clean, min_area=min_area)
    masks = merge_masks(colors, masks)
    masks = filter_edge_mask(masks)

    rects = []
    areas = []
    for mask in masks:
        rects_, areas_ = get_rects_from_mask(mask, min_size=20)
        rects += rects_
        areas += areas_
    return rects, areas


def save_result_to_txt(file_path, rects, areas, width, height, points):

    left = min(points[0][0], points[1][0])
    top = min(points[0][1], points[1][1])
    right = max(points[0][0], points[1][0])
    bottom = max(points[0][1], points[1][1])
    
    ppx = width / (right - left + 1)
    ppy = height / (bottom - top + 1)
    idx_sort = np.argsort(np.array(areas))
    with open(file_path, 'w') as f:
        for idx in idx_sort[::-1]:
            x1, y1, x2, y2 = rects[idx]
            area = areas[idx]
            x1_ = round((x1 - left) * ppx, 1)
            y1_ = round((y1 - top)  * ppy, 1)
            x2_ = round((x2 - left)  * ppx, 1)
            y2_ = round((y2 - top)  * ppy, 1)
            f.write(f'{x1},{y1},{x2},{y2},{area}: {x1_},{y1_},{x2_},{y2_},{round(area*ppx*ppy, 1)}\n')


def color_segmet(image_path, width=None, height=None, points=None, method=2):
    if not image_path.endswith('.png') or not os.path.exists(image_path):
        return
    file_name = os.path.basename(image_path)
    file_dir = image_path.replace(file_name, '')
    file_name = file_name.replace('.png', '.txt')
    result_path = os.path.join(file_dir, file_name)

    segment_method = color_segment_1 if method == 1 else color_segment_2
    image = cv2.imread(image_path)
    rects, areas = segment_method(image)
    
    if points is not None:
        left = min(points[0][0], points[1][0])
        top = min(points[0][1], points[1][1])
        right = max(points[0][0], points[1][0])
        bottom = max(points[0][1], points[1][1])
    
        ppx = width / (right - left + 1)
        ppy = height / (bottom - top + 1)

        result_image_path = image_path.replace('.png', '_result.jpg')
        idx_sort = np.argsort(np.array(areas))
        for idx in idx_sort[::-1]:
            x1, y1, x2, y2 = rects[idx]
            area = areas[idx]
            x1_ = round((x1 - left) * ppx, 1)
            y1_ = round((y1 - top)  * ppy, 1)
            x2_ = round((x2 - left)  * ppx, 1)
            y2_ = round((y2 - top)  * ppy, 1)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(image, f'{round(area*ppx*ppy, 1)}', (x1, y2-25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.putText(image, f'({round(x2_-x1_, 1)},{round(y2_-y1_, 1)})', (x1, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        cv2.imwrite(result_image_path, image)
    
    image_height, image_width = image.shape[:2]
    if width is None or height is None:
        width = image_width
        height = image_height
    if points is None:
        points = [[0, 0], [image_width, image_height]]
    save_result_to_txt(result_path, rects, areas, width, height, points)


def color_segment_runner(image_dir):
    image_info_path = os.path.join(image_dir, 'image_info')
    if not os.path.exists(image_info_path):
        print('image_info is not exist!')
        return
    with open(image_info_path, 'r') as f:
        image_info = ast.literal_eval(f.readline())
    for image_name in image_info.keys():
        image_path = os.path.join(image_dir, image_name)
        if not os.path.exists(image_path):
            print(f'{image_path} not exist!')
            continue
        print(f'processing {image_path}...')
        image_info_ = image_info[image_name]
        width = None if image_info_['width'] == 0 else image_info_['width']
        height = None if image_info_['height'] == 0 else image_info_['height']
        points = None if len(image_info_['points']) < 2 else image_info_['points']
        color_segmet(image_path, width, height, points)


if __name__ == '__main__':
    pass

    # 单独处理一张图像
    # image_path = 'images\image002.png' 
    # color_segmet(image_path)

    # 批量处理
    color_segment_runner('images')


