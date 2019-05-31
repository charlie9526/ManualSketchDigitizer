import sd1
import cv2

def test_detct_shapes():
    image_list = [["test1.jpg",1],["test2.jpg",2],["test3.jpg",3],["test4.jpg",4],["test5.jpg",5]]
    for img in image_list:
        img1 = cv2.imread(img[0])
        length = len(sd1.detct_shapes(img1))
        assert length == img[1]
