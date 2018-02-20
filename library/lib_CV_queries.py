# -*- coding: utf-8 -*-
"""
u
"""
# We use pandas library to read CSV data.
import pandas as pd
import numpy as np
import unicodedata
import os

import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf
import file_operations as fo


def get_people_nopdf (table):
#    indexes = np.where(table["pdf_exists"] == False)[0].tolist()
#    people = table.where(table["pdf_exists"] == False)
#    people = table.where(table == False,table['pdf_exists'], axis='index')
#    people = table.query('pdf_exists == False')
    people = table[table["pdf_exists"] == False]
    
#    print people.shape
    
    return people
    

def copy_people_pdf_by_concept(table, concept = ""):
    
    main_path = "./selected_pdfs/"
    rows = table.index.values.tolist()   # Indexes of rows
    
    for i in rows:
        person = table.ix[i]
        
        if (person["pdf_exists"] == True):  # If the person has pdf
        
            if (concept != ""): # If we are given a concept
                out_path = main_path + str(person[concept]) +"/"
            else:
                out_path = main_path
                
            fo.create_folder_if_needed(out_path)
            fo.copy_pdf_person (out_path, person)
        