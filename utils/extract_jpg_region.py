import os 
import cv2
import re
from glob import glob 
import pytesseract
import numpy as np
from pathlib import Path
import itertools

KERNEL_INT = 48
WIDTH_DILATION = 112 
IMG_KERNEL = (KERNEL_INT, KERNEL_INT)

class BoundingBox ():
    def __init__(self, x,y,w,h, label):
        self.x1= x
        self.y1= y
        self.x2= x+w
        self.y2= y+h
        self.w = w
        self.h = h
        self.label = label
        self.not_overlap = True 

    def __str__ (self):
        return ( str(self.label) + ' : '+ '('+str(self.x1) +', '+str(self.y1)+')'+'\t' + '('+str(self.x2) +', '+str(self.y2)+')')
        
        
def show(im2):
    im2s = cv2.resize(im2, (800,1000)) 
    cv2.imshow('test',im2s)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def check_overlap (b1, b2):
    return (b1.x1 < b2.x2 and b1.x2 > b2.x1 and b1.y1 < b2.y2 and b1.y2 > b2.y1)

#boxes: [ [x,y,w,h]...]
def merge_bounding_boxes(boxes):
    #process so that box list always starts from top left to bottom right
    boxes = sorted(boxes, key=lambda x:(x.y1, x.x1))
    for i in boxes:
        print(i.label)
    for i in range(len(boxes)):
        j = i+1
        while j < len(boxes):
            if (check_overlap(boxes[i],boxes[j])):
#                print(boxes[i].label, boxes[j].label, sep='\t')
                boxes[i].x1 = min(boxes[i].x1, boxes[j].x1)
                boxes[i].y1 = min(boxes[i].y1, boxes[j].y1)
                boxes[i].x2 = max(boxes[i].x2, boxes[j].x2)
                boxes[i].y2 = max(boxes[i].y2, boxes[j].y2)
                del boxes[j]
                j=i+1
                continue
            j+= 1

    return boxes 

#source: https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
def get_bounding_boxes (img, img_kernel = IMG_KERNEL, width_dilation = WIDTH_DILATION) :
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #mat, can show
    #increase contrast

    
    # Performing OTSU threshold 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    # Specify structure shape and kernel size.  
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, img_kernel) 
    # Appplying dilation on the threshold image 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) #mat, can show 
    # Finding contours 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,  
                                                     cv2.CHAIN_APPROX_NONE)
    # Looping through the identified contours
    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        boxes.append( BoundingBox(x,y,w,h,len(boxes)) )  

    #merge bounding boxes
    boxes = merge_bounding_boxes(boxes)
    boxes = sorted(boxes, key = lambda x:(  int(x.w/width_dilation), x.x1, x.y1))
    img2 = img.copy()
    for i in boxes:
        cv2.rectangle(img2, (i.x1, i.y1), (i.x2, i.y2), (0, 255, 0), 2)
        cv2.putText(img2, str(i.label), (i.x1,i.y1+10), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0,0),2)
    show(img2)
    

    
    for i in boxes:
        cv2.rectangle(img, (i.x1, i.y1), (i.x2, i.y2), (0, 255, 0), 2)
        cv2.putText(img, str(i.label), (i.x1,i.y1+10), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0,0),2)
    show(img)

    
    
    #sort contours:
    #first sort by column width, then by x, then y
    #the idea is to mimic human eye pattern to look from top left to bottom left then top right to bottom right 

    
    return boxes 


def extract_jpg_regions (jpg_path, output_dir, img_kernel = IMG_KERNEL, width_dilation = WIDTH_DILATION): 
        img = cv2.imread(jpg_path)
        boxes = get_bounding_boxes(img, img_kernel, width_dilation)
        index = 0
    
        for i in boxes:
            output_path = output_dir +str(index)+'.jpg'
            #get cropped region of image            
            cropped = img[i.y1:i.y2, i.x1:i.x2]
            cv2.resize (cropped,(400, 400))
            #cv2.imwrite(output_path, cropped)                       
            index += 1


   
def extract_from_folder_flat (input_dir, output_dir, img_kernel = IMG_KERNEL, width_dilation = WIDTH_DILATION): 
    jpg_paths = sorted(glob(os.path.join(input_dir,"*.jpg")))
    for jpg_path in jpg_paths:
        print ('extracting', os.path.basename(jpg_path), end = '\t') 
        #create output folder 
        output_folder = output_dir
        extract_jpg_regions (jpg_path, output_folder, img_kernel, width_dilation)

   
def extract_from_folder (input_dir, output_dir, img_kernel = IMG_KERNEL, width_dilation = WIDTH_DILATION):    
    jpg_paths = sorted(glob(os.path.join(input_dir,"*.jpg")))
    for jpg_path in jpg_paths:
        print ('extracting', os.path.basename(jpg_path), end = '\t') 
        #create output folder 
        #get jpg_file_name, all region output will be nested under namesake folder
        jpg_file_name = os.path.basename(jpg_path).rstrip('.jpg')
        if not jpg_file_name:
            print('jpg file name not following convention')
            print('faulty file name:', jpg_file_name)
            raise
        #create folder if it does not exist
        output_folder = output_dir+jpg_file_name+'/'
        if (os.path.exists(output_folder)):
            print('folder exists, skipping') 
            continue
        else:
            Path(output_folder).mkdir(exist_ok=True) #raise error if jpg already visited
            print('to', output_folder)
            #extract image to output folder
            extract_jpg_regions (jpg_path, output_folder, img_kernel, width_dilation)


def main():
    folders = sorted(glob(os.path.join('/home/toto/Desktop/ocr/jpgs', '*')))
    for folder in folders:
        extract_from_folder_flat(folder, '/home/toto/Desktop/ocr/jpg_regions')
#    print(folders)
if __name__ == '__main__':
    main() 
