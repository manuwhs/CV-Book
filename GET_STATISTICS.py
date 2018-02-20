# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya


THIS SCRIPT CALCULATES THE NUMBER OF PEOPLE IN DIFFERENT ASPECTS

"""
# We use pandas library to read CSV data.
import import_folders
import numpy as np

import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf
import file_operations as fo

# Get the dataset 
MasterTable, ds = fo.load_MasterTable_pkl()
year = 2015
# Tabla por Carreras y año: 
indexes = MasterTable.index.tolist()

education = ds["education"]
Neducation = len(education)

# Normalize names
for i in range (Neducation):
    education[i] = CVlib.normalize_text(education[i])
    
    
# We create a subgroup of the degrees, (dictionary with more input than output)

reduced_education = []

Edu_dic = dict(zip(education, range(Neducation)))


start_years = range(2008,year+1)
Nyear = len(start_years)
st_yr_dic = dict(zip(start_years, range(Nyear)))

Infomation_table = np.zeros((Neducation +1 ,Nyear +1))
# The plus 1 is to add the total by column and by row

for i in indexes:
    study = MasterTable["current_studies"][i]
    year_st = MasterTable["start_year"][i]
    
    study = CVlib.normalize_text(study) 
    # Get the indexes
    
    try:
        Edu_indx = Edu_dic[study]
        yr_indx = st_yr_dic[year_st]
        
    except KeyError:
        print i,year_st, study

        continue;
        
    Infomation_table[Edu_dic[study]][st_yr_dic[year_st]] += 1


#  Delete all columns and rows with less than 5:
edusum = np.sum(Infomation_table, axis = 1)
year_sum = np.sum(Infomation_table, axis = 0)

Infomation_table[-1,:] = year_sum
Infomation_table[:,-1] = edusum

Infomation_table[-1,-1] = np.sum(edusum)
# Save BBDD
#fo.save_MasterTable(MasterTable,ds)

# In case you want to see it in the spyder
#MasterTable_list = np.array(MasterTable).tolist()

























#MasterTable, ds = fo.load_MasterTable_pkl()
#
#ds["education"].append("Grado en Ingeniería Eléctrica")
#fo.save_MasterTable(MasterTable,ds)
