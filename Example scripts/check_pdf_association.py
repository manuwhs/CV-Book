# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya
"""
# We use pandas library to read CSV data.
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

# All pdf folders
path_pdfs = "./all_pdfs/"


indexes = MasterTable.index.tolist()
for i in indexes:
    MasterTable["pdf_exists"][i] = False
    
CVlib.set_table_pdf_existance(path_pdfs, MasterTable)

""" WARINING """
######################################
#### THIS REMOVES ALL PEOPLE THAT DONT HAVE AN ASSOCIATED PDF

MasterTable = MasterTable[MasterTable["pdf_exists"] == True]


# Save BBDD
fo.save_MasterTable(MasterTable,ds)

# In case you want to see it in the spyder
MasterTable_list = np.array(MasterTable).tolist()

people_nopdf = CVlibQ.get_people_nopdf(MasterTable)


Selected = MasterTable[MasterTable["pdf_exists"] == True]

print Selected.shape





