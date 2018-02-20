# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf
import file_operations as fo
import lib_CV_queries as CVlibQ

import copy as copy

# Get the dataset 
MasterTable, ds = fo.load_MasterTable_pkl()

folder_in = "./SC14"
folder_out = "./tried"

#indexes = MasterTable.index.tolist()
#for i in indexes:
#    MasterTable["pdf_exists"][i] = False
    
found_flags = CVpdf.rename_CV_files_format1(folder_in,folder_out, MasterTable,1)

found_flags = CVpdf.rename_CV_files(folder_in,folder_out, MasterTable,1)


#indexes = np.where(found_flags[:,0] == 0)[0].tolist()
#people_names = (np.array(people_names)[indexes]).tolist()
#people_name_pdfs = (np.array(people_name_pdfs)[indexes]).tolist()
fo.save_MasterTable(MasterTable,ds)

MasterTable.to_csv("Pene.csv", sep=',')
