# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya

THIS FILE MERGES THE GIVEN FOLDER INTO THE "all_pdfs" FOLDER
WHERE ALL THE PDFS ARE.

You have to indicate the event that the pdfs in the folder are from
so that in case of already having that pdf, it either does nothing or
replaces it

"""
# We use pandas library to read CSV data.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf
import file_operations as fo
import copy as copy

# Get the dataset 
#file_dir = "./data/EBEC15pdfs.csv"

#folder_in = "./Bien/CVs_ordenados/"
#folder_in = "./Bien/td15/"
folder_in = "./Bien/EBEC15/"
#folder_in = "./Bien/prueba/"
origin_table = "EBEC15"

#CVlib.rename_all_pdfs("./Bien/EBEC15/", MasterTable)

# Get the dataset 
MasterTable, ds = fo.load_MasterTable_pkl()

origins = ds["origins"]

fo.merge_pdfs_to_all_pdf (folder_in,origin_table, MasterTable,origins)

            