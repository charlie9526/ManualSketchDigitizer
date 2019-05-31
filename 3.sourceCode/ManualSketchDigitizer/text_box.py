import pytesseract
from pytesseract import Output
import cv2


def text_out(img):
    text_out_output = []
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    img1 = cv2.imread(img)
    n_boxes = len(d['level'])
    final_boxes = []
    for i in range(n_boxes):
        if ((d['text'][i] != '') and (d['text'][i] != ' ')):
            text = (d['text'][i])
            (x, y, w, h) = (d['left'][i], d['top']
                            [i], d['width'][i], d['height'][i])
            text_box = [[x, y], [x + w, y + h]]
            temp = [text_box, text]
            cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 255, 255), -1)
            final_boxes.append(temp)
            #print (pytesseract.image_to_string(img[y:y+w,x:x+w]))
    text_out_output.append(final_boxes)
    text_out_output.append(img1)

    return text_out_output


#img = cv2.imread('kk.jpg')
#k = text_out(img)
#cv2.imshow('img', img)
#print (k)
#cv2.waitKey(0)
