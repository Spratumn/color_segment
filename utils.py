import cv2
import numpy as np

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
    h, w = image.shape[:2]
    
    color_dict = {}
    for i in range(h):
        for j in range(w):
            color = image[i, j, :]
            if is_in_color_range(color, [[0, 5], [0, 5], [0, 5]]):continue
            color_str = f'{color[0]},{color[1]},{color[2]}'
            if color_str not in color_dict:
                color_dict[color_str] = 1
            else:
                color_dict[color_str] += 1
    
    colors = []
    masks = []
    for color_str in color_dict.keys():
        if color_dict[color_str] < min_area:continue
        color = np.array([int(v) for v in color_str.split(',')])
        mask = cv2.inRange(image, color, color)
        colors.append(list(color))
        masks.append(mask)
    return colors, masks


def merge_colors(colors, deviation=5, offset=None):
    merged_colors = []
    single_colors = []

    while len(colors):
        color = colors.pop()
        sub_colors = [color]
        
        base_colors = []
        if offset is not None: 
            for off in offset:
                b_ = color[0] + off
                g_ = color[1] + off
                r_ = color[2] + off
                if max(b_, g_, r_) <= 256 and min(b_, g_, r_) > -2:
                    base_colors.append([b_, g_, r_])
        else:
            base_colors.append(color)

        for (b, g, r) in base_colors:
            b_range = [max(0, b-deviation), min(255, b+deviation)]
            g_range = [max(0, g-deviation), min(255, g+deviation)]
            r_range = [max(0, r-deviation), min(255, r+deviation)]
    
            color_range = [b_range, g_range, r_range]
            
            for idx, color_ in enumerate(colors):
                if is_in_color_range(color_, color_range):
                    colors.pop(idx)
                    sub_colors.append(color_)

        if len(sub_colors) > 1:
            merged_colors.append(sub_colors)
        else:
            single_colors.append(sub_colors[0])
    return merged_colors, single_colors


def merge_masks(colors, masks):

    color_dict = {}
    color_idx = 0
    for (b, g, r) in colors:
        color_str = f'{b},{g},{r}'
        color_dict[color_str] = color_idx
        color_idx += 1
    
    merged_colors, single_colors = merge_colors(colors, deviation=5, offset=[127, -127])
    
    output_masks = []
    for (b, g, r) in single_colors:
        color_str = f'{b},{g},{r}'
        output_masks.append(masks[color_dict[color_str]])
    
    for mask_group in merged_colors:
        (b, g, r) = mask_group[0]
        color_str = f'{b},{g},{r}'
        base_mask = masks[color_dict[color_str]]
        for (b, g, r) in mask_group[1:]:
            color_str = f'{b},{g},{r}'
            base_mask += masks[color_dict[color_str]]
        output_masks.append(base_mask)
    
    return output_masks


def filter_edge_mask(masks):
    filtered_masks = []
    for mask in masks:
        mask_ = cv2.GaussianBlur(np.array(mask), (5, 5), 1)
        ret, thresh = cv2.threshold(mask_, 0, 200, cv2.THRESH_BINARY)
        kernel = np.ones((15, 15),np.uint8)
        thresh = cv2.erode(thresh ,kernel)
        if np.sum(thresh>0) > 50:
            filtered_masks.append(mask)
    return filtered_masks


def nms(rects, iou_thresh=0.7):
    output_rects = []
    while len(rects):
        base_rect = rects.pop(0)
        output_rects.append(base_rect)

        temp_rects = []
        for rect in rects:
            if iou(rect, base_rect) < iou_thresh:
                temp_rects.append(rect)
        rects = temp_rects
    return output_rects


def iou(rect1, rect2):
    x1, y1, x2, y2 = rect1
    area1 = (x2 - x1) * (y2 - y1)
    x1, y1, x2, y2 = rect2
    area2 = (x2 - x1) * (y2 - y1)

    inter_w = min(rect1[2], rect2[2]) - max(rect1[0], rect2[0])
    inter_h = min(rect1[3], rect2[3]) - max(rect1[1], rect2[1])
    inter = 0 if inter_w < 0  or inter_h < 0 else inter_w * inter_h
    return inter / (area1 + area2)


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
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < min_size or h < min_size:
            mask[y:y+h, x:x+w] = 255

    mask_color = np.stack([mask, mask, mask], axis=2)
    image_copy[mask_color>0] = 0

    mask = cv2.inRange(image_copy, np.array([0, 0, 0]), np.array([30, 30, 30]))
    mask_color = np.stack([mask, mask, mask], axis=2)
    image[mask_color>0] = 0

    return image


def get_rects_from_mask(mask, min_size=20):
    
    image_h, image_w = mask.shape[:2]
    mask = cv2.GaussianBlur(mask, (5, 5), 1)

    ret, thresh = cv2.threshold(mask, 0, 200, cv2.THRESH_BINARY)
    kernel = np.ones((7, 7),np.uint8)
    thresh = cv2.dilate(thresh ,kernel)
    
    rects = []
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < min_size or h < min_size:continue
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(image_w-1, x+w)
        y2 = min(image_h-1, y+h)
        rects.append([x1, y1, x2, y2])
    return rects


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



def is_in_color_range(color, color_range):
    assert len(color) == len(color_range)
    
    for i in range(len(color)):
        v_range = color_range[i]
        assert len(v_range) == 2
        assert v_range[0] < v_range[1]
        if color[i] not in range(v_range[0], v_range[1]+1):return False
        
    return True


def vote_filter2d(image, ksize=3):
    h, w = image.shape[:2]
    n_w = w // ksize
    n_h = h // ksize

    out_image = np.array(image)

    for i in range(n_h):
        for j in range(n_w):
            h1 = i * ksize
            h2 = h1 + ksize
            w1 = j * ksize
            w2 = w1 + ksize
            roi = out_image[h1:h2, w1:w2] if len(out_image.shape) == 1 else out_image[h1:h2, w1:w2, :]
            pix_list = []
            for ii in range(ksize):
                for jj in range(ksize):
                    pix = [roi[ii, jj]] if len(out_image.shape) == 1 else list(roi[ii, jj])
                    pix_list.append(','.join([str(v) for v in pix]))
            pix_str = max(set(pix_list), key=pix_list.count)
            pix = int(pix_str) if len(out_image.shape) == 1 else [int(v) for v in pix_str.split(',')]
            for ii in range(ksize):
                for jj in range(ksize):
                    roi[ii, jj] = pix
    return out_image



if __name__ == '__main__':
    image = cv2.imread('images/image001.png')
    cv2.imshow('src', image)
    image1 = vote_filter2d(image, ksize=5)
    cv2.imshow('vote1', image1)
    image2 = vote_filter2d(image, ksize=9)
    cv2.imshow('vote2', image2)
    cv2.waitKey(0)