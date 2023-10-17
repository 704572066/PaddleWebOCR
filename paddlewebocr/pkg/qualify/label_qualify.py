import cv2
import numpy as np
from PIL import Image

from paddlewebocr.pkg.qualify.paddle_detection import det
from paddlewebocr.pkg.util import convert_bytes_to_image


def label_qualify(img_bytes,threshold):
    img = convert_bytes_to_image(img_bytes)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    height, width, _ = img.shape
    img_size = height * width
    array = det(img_bytes)
    label_size = (array[2]-array[0])*(array[3]-array[1])
    ratio = label_size/img_size
    if threshold <= ratio < 1:
        return True, ratio
    return False, ratio
