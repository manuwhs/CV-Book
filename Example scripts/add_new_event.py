# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya


THIS FILE CREATES THE TABLE STRUCTURE OF CV. 
IT DOES NOT ADD ANYONE, JUST CREATES THE TABLE.
"""

import numpy as np
import pandas as pd
import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf
import file_operations as fo
import copy as copy

MasterTable, ds = fo.load_MasterTable_pkl()
#
name = "SC99"
time = 2099

#CVlib.add_new_event(ds,name,time)
ds["education"].append("Grado en Ingeniería Eléctrica")
fo.save_MasterTable(MasterTable,ds)
