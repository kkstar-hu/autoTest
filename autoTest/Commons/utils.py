import cv2


def tran_canny(image):
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return cv2.Canny(image, 50, 150)


def get_distance():
    # 参数0是灰度模式
    image = cv2.imread("2.png", 0)
    template = cv2.imread("1.png", 0)
    # 寻找最佳匹配
    res = cv2.matchTemplate(tran_canny(image), tran_canny(template), cv2.TM_CCOEFF_NORMED)
    # 最小值、最大值、最小值的索引、最大值的索引
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc[0]  # 横坐标
    return top_left
