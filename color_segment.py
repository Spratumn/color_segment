
import os
import cv2
import numpy as np
from utils import *





if __name__ == '__main__':
    source_dir = 'images'
    result_dir = 'results'
    clean_images_dir = 'clean_images'

    image_names = os.listdir(source_dir)

    for image_name in image_names[1:2]:
        if not image_name.endswith(('.png', '.jpg', '.jpeg')):continue
        image_path = os.path.join(source_dir, image_name)
        image = cv2.imread(image_path)
        image_clean = clean_background(image, min_size=20)

        colors, masks = get_sub_masks(image_clean, min_area=400)

        for color, mask in zip(colors, masks):
            print(color)
            cv2.imshow('mask', mask)
            cv2.waitKey(0)


        # for (x1, y1, x2, y2) in rects:
        #     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # cv2.imwrite(os.path.join(result_dir, image_name), image)
        # cv2.imwrite(os.path.join(clean_images_dir, image_name), image_clean)