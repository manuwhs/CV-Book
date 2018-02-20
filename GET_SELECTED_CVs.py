# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya
"""
# We use pandas library to read CSV data.
import import_folders

import lib_CV_Book as CVlib
import CV_book_pdf_lib as CVpdf
import file_operations as fo
import lib_CV_queries as CVlibQ

import copy as copy

MasterTable, ds = fo.load_MasterTable_pkl()

###########################################################################
########### SELECT THE DESIRED CVs #########################################
##############################################################################

Selected = MasterTable
#Selected = MasterTable[MasterTable["origin"] != "EBEC15"]
#Selected = Selected[Selected["origin"] != "TD15"]
#Selected = Selected[Selected["origin"] != "TD14"]
Selected = Selected[Selected["current_studies"] != "Grado en Ingeniería Informática"]
Selected = Selected[Selected["start_year"] > 2013]
Selected = Selected[Selected["pdf_exists"] == True]

#####################################################
""" CREATE THE SS with the SELECTED """
########################################################

Selected = copy.deepcopy(Selected)
indexes = Selected.index.tolist()

# Insert the PDF name into the csv
Selected["pdfname"] = ""
for i in indexes:
    name_pdf = CVlib.get_CVpdf_name(Selected.ix[i])
    Selected["pdfname"][i] = name_pdf

print Selected.shape

Selected.to_csv("./Selected_pdfs.csv")

#####################################################
""" Copy the selected PDFs in folders by the given concept """
########################################################

# selected
concept = ""  
concept = "current_studies"   
#concept = "origin"
#concept = "start_year"


# Only for the people that has an associated pdf
CVlibQ.copy_people_pdf_by_concept(Selected, concept = concept)