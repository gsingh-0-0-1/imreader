from PIL import Image
import pytesseract
import cv2
import os
import numpy as np
import sys
import matplotlib.pyplot as plt


def contrast_filter(img, b, c, offset):
	img = c / (1 + b ** ( -(img + offset) ) )
	img = np.array(img, dtype=int)
	return np.array(img, dtype=int)

def hard_assign(img, center):
	#img = np.mean(img, axis = 2)
	newimg = np.zeros(img.shape, dtype=int)
	newimg[np.where(img <= center)] = 0
	newimg[np.where(img > center)] = 255
	newimg = np.stack((newimg,)*3, axis=-1)
	return newimg

def convert_to_text(path, lang):
	img = cv2.imread(path)
	img = np.array(img)

	mean, median, std = np.mean(img), np.median(img), np.std(img)

	center = mean
	c = 255
	offset = -(255-center)
	b = 1.05

	offset = offset

	img = np.mean(img, axis=2)
	img = np.array(img, dtype=int)

	img = contrast_filter(img, b, c, offset)
	newimg = hard_assign(img, np.mean(img))


	#Add a border to the image
	height = newimg.shape[0]
	width = newimg.shape[1]
	sidebuffer = np.full((height, int(width / 10), 3), 255)

	newimg = np.concatenate((sidebuffer, newimg, sidebuffer), axis=1)

	height = newimg.shape[0]
	width = newimg.shape[1]
	topbuffer = np.full((int(height / 10), width, 3), 255)

	newimg = np.concatenate((topbuffer, newimg, topbuffer), axis=0)

	newimg = np.array(newimg, dtype=np.uint8)

	#newname = "optimized_" + n

	#cv2.imwrite(newname, newimg)
	#img = Image.open(newname)#cv2.imread(newname)

	text = pytesseract.image_to_string(Image.fromarray(newimg), lang=lang, config="load_system_dawg F load_frew_dawg F load_punc_dawg F load_number_dawg F load_unambig_dawg F load_bigram_dawg F load_fixed_length_dawgs F")

	return text

