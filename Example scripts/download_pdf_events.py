# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya

THIS FILE READS A CSV WITH AT LEAST THE INFORMATION:
    full_name
    birthday
    url

It can also contain others

And then tries to download all of them and name them using the BBDD convention.
There may be some "pdfs" you will not be able to download, for example because 
the website does not allow bots to download them.

If there were pdfs that couldnt be downloaded, the program creates a csv
with all the url and the names you have to give them. Someone has to manually
donwload them and name them properly

"""
# We use pandas library to read CSV data.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf

import copy as copy
import time

# Get the dataset 
file_dir = "./data/EBEC15pdfs.csv"
#file_dir = "./data/TTDpdfs.csv"
folder_out = "./pene/"

###### Load and normalize table  #######
table_CV = CVlib.load_dataset(file_dir)
CVlib.normalize_birthday(table_CV)
CVlib.normalize_full_names(table_CV)
CVlib.replance_NaN_NULL(table_CV)



NotDownloadedTable = CVpdf.download_pdfs_table (table_CV, folder_out)

NotDownloadedTable.to_csv("./NotDownloadedTable.csv", sep=',')


