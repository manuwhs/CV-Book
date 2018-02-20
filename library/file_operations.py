# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 01:31:58 2015

@author: montoya
"""
from sklearn.cross_validation import StratifiedKFold  # For crossvalidation
import numpy as np
import matplotlib.pyplot as plt

import os.path

import pickle_lib as pkl
import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf
import lib_CV_queries as CVlibQ

import pandas as pd
########################################################################
################### Save Results ######################
#######################################################################

def save_MasterTable(MasterTable, dictionaries, partitions = 1):
    path = "./BBDD/"
    filename_pkl = "MasterTable"
    filename_SS = "MasterTable_SS.csv"
    
    # Create csv from table
    MasterTable.to_csv(path + filename_SS, sep=',')
    
    content_pkl = [MasterTable, dictionaries]
    # Save Whole BBDD with dictionaries in pkl
    pkl.store_pickle(path + filename_pkl, content_pkl, partitions = 1)
    
    print "MasterTable saved"

def load_MasterTable_pkl(l = 1):
    path = "./BBDD/"
    filename_pkl = "MasterTable"
    
    loaded = pkl.load_pickle(path + filename_pkl ,l)
    MasterTable = loaded[0]
    dictionaries = loaded[1]

    CVlib.replance_NaN_NULL(MasterTable)
    CVlib.normalize_birthday(MasterTable)
    CVlib.normalize_full_names(MasterTable)
    
    print "MasterTable_pkl loaded"
    
    return MasterTable, dictionaries

def load_MasterTable_SS():
    path = "./BBDD/"
    filename_SS = "MasterTable_SS.csv"
    
    table_SS = pd.read_csv(path + filename_SS, sep = ',', index_col = 0) 
    CVlib.replance_NaN_NULL(table_SS)
    CVlib.normalize_birthday(table_SS)
    CVlib.normalize_full_names(table_SS)
    
    print "MasterTable_SS loaded"
    
    return table_SS
    
def modify_pdf_from_csv(l = 1):
    # This function aims to modify the columns of the BBDD reading
    # from a CSV with at least the names and bdays.
    # YOU CANNOT CHANGE NAMES AND BDAYS !!

    path = "./BBDD/"
    filename_pkl = "MasterTable"
    
    loaded = pkl.load_pickle(path + filename_pkl ,l)
    MasterTable = loaded[0]
    dictionaries = loaded[1]
    
    print "MasterTable_pkl loaded"
    
    return MasterTable, dictionaries
    
    
########################################################################
################### Load without repetition (obsolete) ######################
#######################################################################


import shutil

def copy_pdf_person (folder, person):
    # Copies the pdf of a person in the given folder
    folder_in = "./all_pdfs/"
    
    if (person["pdf_exists"] == True):
        name_pdf = CVlib.get_CVpdf_name(person)
        shutil.copy2(folder_in + name_pdf, folder + name_pdf)
        
    else:
        print "The person " + person["full_name"] + " has no pdf"

def merge_pdfs_to_all_pdf (folder_in,origin_table, MasterTable,origins):
    folder_out = "./all_pdfs/"
    
    # Puts the pdfs into the main folder only if they already exist in the BBDD SS
    # and if there is no newer copy of them.
    
    for dirName, subdirList, fileList in os.walk(folder_in):  # FOR EVERY DOCUMENT
        for fname in fileList:
            path_in = dirName + '/' + fname;  # The path of the input pdf
            # Obtain the name and bday of the person associated with the pdf we want to add
            # We check if the file names already have the index or not first.
            # if they dont have them coz thay just were downloaded we get the index from the table
            
            if (len (fname.split("_")) == 2):
                full_name, birthday = CVlib.get_person_namebday_from_pdfname(fname) 
                index = CVlib.get_person_indx(MasterTable, full_name, birthday)
            else:
                full_name, birthday,index = CVlib.get_person_indexes_from_pdfname(fname) 
                
            if (index == -1):  # If the person does not exist, we dont add the pdf
                print fname + " didnt have anyone in the MasterTable"
                break;
                
            else:
            # Before adding the pdf we have to change its name adding the index, if needed
            # Check if the pdf is older, in that case we dont add it.
                old_person = MasterTable.ix[index]
                fname_new = CVlib.get_CVpdf_name(old_person)
                
                exist = os.path.exists(folder_out + fname_new)  # Check if the file
                
                if (exist == 0):  # If the file does not exist, we just add it
                    shutil.copy2(path_in, folder_out + fname_new)
                
                else: #If it already exists we check if it is newer 
                    origin_old = old_person["origin"]
                    origin_new = origin_table
                        
                    date_old = origins[1][origins[0].index(origin_old)]
                    date_new = origins[1][origins[0].index(origin_new)]
        
                    if (date_new >= date_old):  # If the pdf is newer than the one already in the main folder
                        shutil.copy2(path_in, folder_out + fname_new)
                        print fname_new + " updated"
            
def create_folder_if_needed (folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
