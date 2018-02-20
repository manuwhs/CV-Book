# -*- coding: utf-8 -*-
"""
u
"""
# We use pandas library to read CSV data.

import import_folders

import os

import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf
import file_operations as fo


# Extract jpg's from pdf's. Quick and dirty.

fo.create_folder_if_needed ("./images/")

folder_in = "./all_pdfs/"
for dirName, subdirList, fileList in os.walk(folder_in):  # FOR EVERY DOCUMENT
    for fname in fileList:
        # Read the file
        path = dirName + '/' + fname;
        
        input_file = file(path, "rb")
        pdf = input_file.read()
        
        startmark = "\xff\xd8"
        startfix = 0
        endmark = "\xff\xd9"
        endfix = 2
        i = 0
        njpg = 0
        
        while True:
            
            istream = pdf.find("stream", i)
            
            if istream < 0:
                break
            
            if (njpg > 0):
                break
            
            istart = pdf.find(startmark, istream, istream+20)
            
            if istart < 0:
                i = istream + 20
                continue
            
            iend = pdf.find("endstream", istart)
            
            if iend < 0:
                raise Exception("Didn't find end of stream!")
                
            iend = pdf.find(endmark, iend - 20)
            if iend < 0:
                raise Exception("Didn't find end of JPG!")
             
            istart += startfix
            iend += endfix
            
            print "JPG %d from %d to %d" % (njpg, istart, iend)
            
            jpg = pdf[istart:iend]
            
            jpgname = "./images/" + fname + str(njpg)+ ".jpg"
            jpgfile = file(jpgname, "wb")
            jpgfile.write(jpg)
            jpgfile.close()
            
            i = iend
        #    break
        
            njpg += 1





#
#content = ""
## Load PDF into pyPDF
#input_file = file(path, "rb")
#pdf = PdfFileReader(input_file)
#
## Iterate pages
#for i in range(0, pdf.getNumPages()):
#    # Extract text from page and add to content
#    page = pdf.getPage(i)
#    content += pdf.getPage(i).extractText() + "\n"
#
#con = page.getContents()
#obj = page.getObject()
#res = obj["/Resources"]
#
## Collapse whitespace
#content = " ".join(content.replace(u"\xa0", " ").strip().split())
#input_file.close()




    
        