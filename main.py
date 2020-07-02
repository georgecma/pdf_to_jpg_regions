from utils.convert_pdf import convert_pdfs
from utils.extract_jpg_region import extract_from_folder, extract_from_folder_flat
from utils.classify_region import classify_folder
from glob import glob 
import os 

pdf_dir = 'pdfs/'
jpg_dir = 'jpgs/'
jpg_region_dir = 'jpg_regions/'
kernel_int = 56
kernel_box = (kernel_int, kernel_int)

def main():
#    convert_pdfs (pdf_dir, jpg_dir)

    jpg_folders = sorted (glob(os.path.join(jpg_dir, '*')))
    for jpg_folder in jpg_folders:
        extract_from_folder (jpg_folder, jpg_region_dir, kernel_box)

    
if __name__ == '__main__':
    main() 


