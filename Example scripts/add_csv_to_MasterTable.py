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
import copy as copy

# Get the dataset 
MasterTable, ds = fo.load_MasterTable_pkl()

#tables_dir = ["./data/CV_Book.csv",
#            "./data/EBEC15.csv",
#            "./data/BESTIES.csv",
#            "./data/TD15.csv"
#            ]

tables_dir = ["./data/EBEC15.csv"]
""" ADD THE TABLES """

for csv_dir in tables_dir:
    people_table = CVlib.load_and_preprocess_csv(csv_dir)
    CVlib.add_to_whole_table(MasterTable,people_table, ds["origins"])

# Save BBDD
fo.save_MasterTable(MasterTable,ds)

# In case you want to see it in the spyder
#MasterTable_list = np.array(MasterTable).tolist()
