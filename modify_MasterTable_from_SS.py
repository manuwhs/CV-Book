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
origins = ds["origins"]

MasterTable_SS_modified = fo.load_MasterTable_SS()
index_modified = MasterTable_SS_modified.index.tolist()
#
for i in index_modified:
    person_mod = MasterTable_SS_modified.ix[i]
    CVlib.modify_person(MasterTable, person_mod, origins)
    

#CVlib.remove_all_shit_spaces(MasterTable, "current_studies")

# Save BBDD
fo.save_MasterTable(MasterTable,ds)

# In case you want to see it in the spyder
#MasterTable_list = np.array(MasterTable).tolist()



# Print into a csv everyone that does not have a pdf associated

nppdf = MasterTable[MasterTable["pdf_exists"] == False]

## COPY AND DO
nppdf = copy.deepcopy(nppdf)
indexes = nppdf.index.tolist()

nppdf["pdfname"] = ""

for i in indexes:
    name_pdf = CVlib.get_CVpdf_name(nppdf.ix[i])
    nppdf["pdfname"][i] = name_pdf

print nppdf.shape

nppdf.to_csv("./People_with_no_pdf.csv")

