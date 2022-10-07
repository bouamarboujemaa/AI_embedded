 """
 * @file        test_yolo_annotation.py
 * @version     1.0
 * @author      BOUAMOR BOUJEMAA
 * @date        2022.05.22
 """

import cv2
import matplotlib.pyplot as plt


img = cv2.imread('1.png')
dh, dw, _ = img.shape

fl = open('1.csv', 'r')
data = fl.readlines()
fl.close()

for dt in data:

    _, x, y, w, h = map(float, dt.split(' '))

    l = int((x - w / 2) * dw)
    r = int((x + w / 2) * dw)
    t = int((y - h / 2) * dh)
    b = int((y + h / 2) * dh)


    cv2.rectangle(img, (l, t), (r, b), (0, 255, 255), 3)


plt.imshow(img)
plt.show()
#cv2.imshow("image", img)
#cv2.waitKey(0)


