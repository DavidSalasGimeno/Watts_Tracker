import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def org_core(img):
	text = pytesseract.image_to_string(img) # Search text in images
	return text



def img_cropper(img):
		
	height, width, channels = img.shape # Get images dimensions
	first =  int(height/10*5.5) # Selects the height where to start scanning
	second = int(height/10*6.5) # Selects the height where must finish the scanning

	return img[first:second , 0:width] # Returns an image cropped



def whitespace_cropper(img): # Crop white spaces in the image
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # To invert the text to white
	gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
	coords = cv2.findNonZero(gray) # Finds all non-zero points (text)
	x, y, w, h = cv2.boundingRect(coords) # Finds minimum spanning bounding box
	img = img[y:y+h, x:x+w] # Crops the image - note we do this on the original image
	height, width, channels = img.shape # Gets images dimensions
	first =  int(height/10*5.5) # Selects the height where to start scanning
	second = int(height/10*7.25) # Selects the height where must finish the scanning

	return img[first:second , 0:width] # Returns an image cropped


def cost_getter(information, cost = ''): # Selects the numbers of the kWh cost
	for i in information: 
		try:
			if len(cost) >2:
				break
			if i in '0123456789':
				cost += str(i)
		except:
			pass
		
	try:
		cost = int(cost)

		if 50<cost<500:

			return cost
	except:
		pass


def exceptional_case(img):
		
	height, width, channels = img.shape # Get images dimensions
	first =  int(height/10*5) # Selects the height where to start scanning
	second = int(height/10*10) # Selects the height where must finish the scanning
	img = img[0:height , int(width/2):width] # Returns an image cropped
	
	return img
	



def read_img(img_file_name):
	original_img = cv2.imread(str(img_file_name)+'.jpg') # Loads the image in memory


	cropped_img = img_cropper(original_img)	
	information = org_core(cropped_img)
	cost = cost_getter(information)

	if cost: # Checks if the functions before has found the cost
		return cost
	

	cropped_img = whitespace_cropper(original_img)
	information = org_core(cropped_img)	
	cost = cost_getter(information)
	
	
	if cost: # Checks if the functions before has found the cost
		return cost

	cropped_img = exceptional_case(cropped_img)
	information = org_core(cropped_img)	
	cost = cost_getter(information)

	if cost: # Checks if the functions before has found the cost
		return cost

