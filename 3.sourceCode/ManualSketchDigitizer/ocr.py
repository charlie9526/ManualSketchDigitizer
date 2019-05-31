from PIL import Image
import pytesseract

#this is the function of OCR
def read_text(image):
	#image wanted to OCR
	im = Image.open(image)
	#OCR is done by pytesseract 
	text = pytesseract.image_to_string(im, lang = 'eng')
	return text


