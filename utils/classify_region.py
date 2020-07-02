
import os
import cv2
from glob import glob
import pytesseract
import pandas as pd 
import numpy as np

input_dir = 'jpg_regions/'

def show(im2):
#    im2s = cv2.resize(im2, (900,1200)) 
    cv2.imshow('test',im2)
    cv2.waitKey(0)

def classify_jpg (path) :
    img = cv2.imread(path)

    df = pytesseract.image_to_data(img, output_type='data.frame')

    #placeholder method for detecting charts vs imgs
    average_conf = np.mean(df['conf'])
    if (average_conf < 50 ) :
        return -1
    else:
        return 1
        

def classify_folder(path):
    jpg_paths = sorted(glob(os.path.join(path, '*')))
    for path in jpg_paths:
    	classify_jpg (path)

def main():
    pass
#    folders = sorted(glob(os.path.join(input_dir, "*")))

#    for folder in folders:
    folder = folders [1]
    classify_folder(folder)

if __name__ == '__main__':
    main()

