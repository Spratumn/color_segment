import cv2
import numpy as np
import time
import random

def detect_rect(mask):
    
    edge = cv2.Canny(mask, 0, 250)
    minLineLength = 100
    maxLineGap = 100
    lines = cv2.HoughLinesP(edge, 1, np.pi / 4, 100, minLineLength, maxLineGap)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    if lines is not None:

        for x1, y1, x2, y2 in lines.reshape(-1, 4):
            cv2.line(mask, (x1, y1), (x2, y2), (0, 255, 0), 4)
    return True if lines is not None else False


def get_sub_masks(image, min_area=500):

    masks = []
    colors = []
    h, w = image.shape[:2]
    color_to_idx = {}
    id_to_color = {}
    idx = 0
    start = time.time()
    for i in range(h):
        for j in range(w):
            color = image[i, j, :]
            if in_color_range(color, [[0, 5], [0, 5], [0, 5]]):continue
            color_str = f'{color[0]},{color[1]},{color[2]}'
            if color_str not in color_to_idx:
                mask = cv2.inRange(image, color, color)
                if np.sum(mask == 255) < min_area:
                    color_to_idx[color_str] = -1
                else:
                    masks.append(mask)
                    colors.append(color_str)
                    color_to_idx[color_str] = idx
                    id_to_color[idx] = color_str
                    idx += 1
                    
    return colors, masks


def merge_masks(colors, masks):
    mask_dict = {}
    for idx, color in enumerate(colors):
        mask_dict[color] = masks[idx]
    
    diff_colors = [[127, 127, 127],
                   [128, 128, 128],
                   [128, 127, 127],
                   [127, 128, 127],
                   [127, 127, 128],
                   [127, 128, 128],
                   [128, 127, 128],
                   [128, 128, 127],
                   [-127, -127, -127],
                   [-128, -128, -128],
                   [-128, -127, -127],
                   [-127, -128, -127],
                   [-127, -127, -128],
                   [-127, -128, -128],
                   [-128, -127, -128],
                   [-128, -128, -127]]

    meraged_masks = []
    for i, color in enumerate(colors):
        color_value = [int(v) for v in color.split(',')]
        
        for db, dg, dr in diff_colors:
            vb = max(min(color_value[0] + db, 255), 0)
            vg = max(min(color_value[1] + dg, 255), 0)
            vr = max(min(color_value[2] + dr, 255), 0)
            search_color = f'{vb},{vg},{vr}'
            if search_color in colors:
                meraged_masks.append(mask_dict[color]+mask_dict[search_color])
                colors.pop(i)
                break
    return meraged_masks


def iou(rect1, rect2):
    x1, y1, x2, y2 = rect1
    area1 = (x2 - x1) * (y2 - y1)
    x1, y1, x2, y2 = rect2
    area2 = (x2 - x1) * (y2 - y1)
    left = max(rect1[0], rect2[0])
    top = max(rect1[1], rect2[1])
    right = min(rect1[2], rect2[2])
    bottom = min(rect1[3], rect2[3])
    return (right-left)*(bottom-top) / (area1 + area2)


def clean_background(image, min_size=10):
    h, w = image.shape[:2]
    mask = np.zeros((h, w), np.uint8)

    for i in range(h):
        for j in range(w):
            color = image[i, j, :]
            if color[0] == color[1] == color[2]:
                mask[i, j] = 255
            elif max(color) - min(color) < 10:
                mask[i, j] = 255

    mask_black = cv2.inRange(image, np.array([0, 0, 0]), np.array([120, 120, 120]))
    mask_white = cv2.inRange(image, np.array([230, 230, 230]), np.array([255, 255, 255]))
    mask += mask_white + mask_black

    mask_color = np.stack([mask, mask, mask], axis=2)
    image_copy = np.array(image)
    image_copy[mask_color>0] = 0

    image_copy = cv2.medianBlur(image_copy, 5)
    gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 200, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    black = np.ones((h, w, 3), np.uint8) * 255
    for cnt in contours:
        color_ = (random.randint(0, 255), random.randint(0, 255),random.randint(0, 255))
        x, y, w, h = cv2.boundingRect(cnt)
        if w < min_size or h < min_size:
            cv2.rectangle(black, (x, y), (x+w, y+h), color_, 1)
            mask[y:y+h, x:x+w] = 255

    mask_color = np.stack([mask, mask, mask], axis=2)
    image_copy[mask_color>0] = 0

    mask = cv2.inRange(image_copy, np.array([0, 0, 0]), np.array([30, 30, 30]))
    mask_color = np.stack([mask, mask, mask], axis=2)
    image[mask_color>0] = 0
    # image[mask_color==0] = 255

    return image



def get_rects_from_gray_image(gray_image, min_size=20):
    
    image_h, image_w = gray_image.shape[:2]

    ret, thresh = cv2.threshold(gray_image, 0, 200, cv2.THRESH_BINARY)
    kernel = np.ones((15, 15),np.uint8)
    thresh = cv2.erode(thresh ,kernel)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < min_size or h < min_size:continue
        x1 = max(0, x-5)
        y1 = max(0, y-5)
        x2 = min(image_w-1, x+w+5)
        y2 = min(image_h-1, y+h+5)
        rects.append([x1, y1, x2, y2])
    return rects



def in_color_range(color, color_range):
    assert len(color) == len(color_range)
    
    for i in range(len(color)):
        v_range = color_range[i]
        assert len(v_range) == 2
        assert v_range[0] < v_range[1]
        if color[i] not in range(v_range[0], v_range[1]):return False
        
    return True
