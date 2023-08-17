import math

import cv2
import numpy as np
from matplotlib import pyplot as plt
# 配置数据
class Config:
    def __init__(self):
        pass

    # src = "images/1.jpg"
    resizeRate = 1
    min_area = 10000
    min_contours = 8
    threshold_thresh = 120
    epsilon_start = 10
    epsilon_step = 10

def binarize(img):
    """画像を2値化する
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 2)
    plot_img(binary_img, 'binary_img')
    return binary_img


def noise_reduction(img):
    """ノイズ処理(中央値フィルタ)を行う
    """
    median = cv2.medianBlur(img, 9)
    plot_img(median, 'median')
    return median


def find_contours(img):
    """輪郭の一覧を得る
    """
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def approximate_contours(img, contours):
    """輪郭を条件で絞り込んで矩形のみにする
    """
    height, width, _ = img.shape
    img_size = height * width
    approx_contours = []
    for i, cnt in enumerate(contours):
        arclen = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        if arclen != 0 and img_size*0.02 < area < img_size*0.9:
            approx_contour = cv2.approxPolyDP(cnt, epsilon=0.05*arclen, closed=True)
            if len(approx_contour) == 4:
                approx_contours.append(approx_contour)
    return approx_contours


def draw_contours(img, contours, file_name):
    """輪郭を画像に書き込む
    """
    draw_contours_file = cv2.drawContours(img.copy(), contours, -1, (0, 0, 255, 255), 10)
    plot_img(draw_contours_file, file_name)


def plot_img(img, file_name):
    """画像の書き出し
    """
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(file_name)
    plt.show()
    cv2.imwrite('./{}.png'.format(file_name), img)


# 找出外接四边形, c是轮廓的坐标数组
def boundingBox(idx, c):
    if len(c) < Config.min_contours:
        return None
    epsilon = Config.epsilon_start
    while True:
        approxBox = cv2.approxPolyDP(c, epsilon, True)
        # 求出拟合得到的多边形的面积
        theArea = math.fabs(cv2.contourArea(approxBox))
        # 输出拟合信息
        print("contour idx: %d ,contour_len: %d ,epsilon: %d ,approx_len: %d ,approx_area: %s" % (
        idx, len(c), epsilon, len(approxBox), theArea))
        if (len(approxBox) < 4):
            return None
        if theArea > Config.min_area:
            if (len(approxBox) > 4):
                # epsilon 增长一个步长值
                epsilon += Config.epsilon_step
                continue
            else:  # approx的长度为4，表明已经拟合成矩形了
                # 转换成4*2的数组
                approxBox = approxBox.reshape((4, 2))
                return approxBox
        else:
            print("failed to find boundingBox,idx = %d area=%f" % (idx, theArea))
            return None

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect
# 求两点间的距离
def point_distance(a, b):
    return int(np.sqrt(np.sum(np.square(a - b))))

def get_perspective_transform(img, approxBox):
    # 获取最小矩形包络
    rect = cv2.minAreaRect(approxBox)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    box = box.reshape(4, 2)
    box = order_points(box)
    print("boundingBox：\n", box)

    # 待切割区域的原始位置，
    # approxPolygon 点重排序, [top-left, top-right, bottom-right, bottom-left]
    src_rect = order_points(approxBox)
    print("src_rect：\n", src_rect)

    w, h = point_distance(box[0], box[1]), point_distance(box[1], box[2])
    print("w = %d ,h= %d " % (w, h))

    # 生成透视变换矩阵
    dst_rect = np.array([
        [0, 0],
        [w - 1, 0],
        [w - 1, h - 1],
        [0, h - 1]],
        dtype="float32")

    # 透视变换
    M = cv2.getPerspectiveTransform(src_rect, dst_rect)

    # 得到透视变换后的图像
    warped_img = cv2.warpPerspective(img, M, (w, h))
    # cv2.namedWindow("perspective_transform", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("perspective_transform", 600, 800)
    # cv2.imshow("perspective_transform", warped)
    # cv2.waitKey(0)
    return warped_img
def get_receipt_contours(img):
    """矩形検出までの一連の処理を行う
    """
    # print("len:%d " % (len(img)))
    plot_img(img, 'img')
    binary_img = binarize(img)
    binary_img = noise_reduction(binary_img)
    contours = find_contours(binary_img)
    approx_contours = approximate_contours(img, contours)
    wraped_img = None
    if len(approx_contours) > 0:
        draw_contours(img, contours, 'draw_all_contours')
        draw_contours(img, approx_contours, 'draw_rectangle_contours')
        max_area_contour = sorted(approx_contours, key=cv2.contourArea, reverse=True)[:1]
        draw_contours(img, max_area_contour, "max_area_contour")
        max_area_contour = max_area_contour[0].reshape((4, 2))
        wraped_img = get_perspective_transform(img, max_area_contour)
    return wraped_img

#
# input_file = cv2.imread('../../images/ford/4.jpg')
# get_receipt_contours(input_file)