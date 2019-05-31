import cv2
import numpy as np

# Normal routines
#img = cv2.imread('ws.png')


def detct_shapes(img):
    #img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 50, 255, 1)

    # Remove some small noise if any.
    dilate = cv2.dilate(thresh, None)
    erode = cv2.erode(dilate, None)

    # Find contours with cv2.RETR_CCOMP
    contours, hierarchy = cv2.findContours(
        erode, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    image_subs = []
    for i, cnt in enumerate(contours):
        # Check if it is an external contour and its area is more than 100
        if hierarchy[0, i, 3] == -1 and cv2.contourArea(cnt) > 100:
            detail = []
            x, y, w, h = cv2.boundingRect(cnt)
            img_inst = img[y-10:y+h+10, x-10:(x+w+10)]
            detail.append([[x-10, y-10], [x+w+10, y+h+10]])
            detail.append(img_inst)
            image_subs.append(detail)
            cv2.rectangle(img, (x-10, y-10), (x+w+10, y+h+10),
                          (255, 255, 255), 2)
            #k = 'sofsqure'+str(x)+'.png'
            #cv2.imwrite("asa.jpg", img)

    return image_subs

