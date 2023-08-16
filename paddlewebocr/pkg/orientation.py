from pytesseract import Output
import pytesseract
import cv2
import numpy as np
def rotate_bound(image, angle):
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH))

# image = cv2.imread('../../images/y.png')

def orientation_detect(image):
    try:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)
        print("[INFO] detected orientation: {}".format(
            results["orientation"]))
        print("[INFO] rotate by {} degrees to correct".format(
            results["rotate"]))
        print("[INFO] detected script: {}".format(results["script"]))
        rotated = rotate_bound(image, angle=results["rotate"])
        cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Original", 600, 800)
        cv2.namedWindow('Original', 0)
        cv2.imshow("Original", image)
        cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Output", 600, 800)
        cv2.namedWindow('Output', 0)
        cv2.imshow("Output", rotated)
        cv2.waitKey(0)
        return rotated
    except:
        return None
#
# image = cv2.imread('../../images/ford/1.jpg')
# orientation_detect(image)
