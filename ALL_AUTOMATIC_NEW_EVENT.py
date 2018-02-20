# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya


THIS SCRIPT IS SUPOSED TO DO EVERYRHING AUTOMATICALLY.
THIS FILE READS A CSV WITH AT LEAST THE INFORMATION:
    full_name
    birthday
    pdfurl

You only have to indicate:
    The path of the csv
    The name of the new event
    The time of the new event

"""
import import_folders

import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf
import file_operations as fo
import copy as copy

# Get the dataset 
MasterTable, ds = fo.load_MasterTable_pkl()
folder_downs = "./down_pdfs/"

## PARAMETERS
csv_dir = "./data/EBEC15all.csv"
name_event = "EBEC15"
time_event = 2015

################# Start action

download_path = folder_downs+ name_event +"/"
fo.create_folder_if_needed (download_path)

# Load the csv
table_CV = CVlib.load_and_preprocess_csv(csv_dir)
indexes = table_CV.index.tolist()

# Include the new event into the list
CVlib.add_new_event(ds,name_event,time_event)

# Add the people to the MasterCSV
# For that first we only select the columns that are in MasterTable
cols_Master = MasterTable.columns.values.tolist()
cols_new_table = table_CV.columns.values.tolist()

common_columns = list(set(cols_Master).intersection(cols_new_table))

table_CV_filtered = table_CV[common_columns]
CVlib.add_to_whole_table(MasterTable,table_CV_filtered, ds["origins"])

# Downlad the pdfs:
NotDownloadedTable = CVpdf.download_pdfs_table (table_CV, download_path)
NotDownloadedTable.to_csv(folder_downs +"NotDownloadedTable.csv", sep=',')

# Include the pdf downloaded to the mail all_pdfs
origins = ds["origins"]
fo.merge_pdfs_to_all_pdf (download_path,name_event, MasterTable,origins)

# Check the asscociation between them
path_pdfs = "./all_pdfs/"
CVlib.set_table_pdf_existance(path_pdfs, MasterTable)

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



# Save BBDD
fo.save_MasterTable(MasterTable,ds)

# In case you want to see it in the spyder
#MasterTable_list = np.array(MasterTable).tolist()
