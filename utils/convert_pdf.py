import os
import sys
from glob import glob
from pdf2image import convert_from_path
from pathlib import Path


#input_path = 'pdfs/'
#output_path = 'jpgs/'

#directory of pdfs 
def convert_pdfs (input_path, output_path): 
    pdf_paths = sorted(glob(os.path.join(input_path,"*.pdf")))
    
    for path in pdf_paths:
        #create new folder in output path and dump images 
        output_folder = os.path.join (output_path, os.path.basename(path))
        print('converting', os.path.basename(path), end = '\t')
        if os.path.exists(output_folder): 
            print('pdf folder exists, skipping')
            continue
        else:
            output_file_name = os.path.basename(path)
            Path(output_folder).mkdir(parents=True, exist_ok=True) 
            convert_from_path(path, dpi=300, output_folder=output_folder,
                              output_file = output_file_name, fmt='jpg')
            print ('pdf converted to', output_folder)
        

def main() :
#    convert_pdfs ('../pdfs/', '../jpgs/')
    pass 
if __name__ == '__main__':
    main() 
