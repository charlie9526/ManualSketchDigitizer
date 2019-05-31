import ocr 

def test_read_text():
    image_list = [["test1.jpeg","we are boys"],["test.jpg","i love you\n\nds"],["test2.jpeg","gindara samaga sellam"],["test3.jpg","keels\nwe care always"],["test4.jpg",""],["test5.jpg","picture 123456"]]
    for img in image_list:
        assert ocr.read_text(img[0])==img[1]
        
        

