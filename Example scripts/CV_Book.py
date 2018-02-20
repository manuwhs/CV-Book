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

import copy as copy

origins = [
	["EBEC13", 2013],
	["TD14", 2014],
	["SC14", 2014],
	["EBEC14", 2014],
	["TTD15", 2015],
	["EBEC15", 2015],
	["BESTIE", 9999]   # BESTies al poder
 ]

origins = np.array(origins).T.tolist()

# Get the dataset 
file_dir = "./data/CV_Book.csv"
people_table = CVlib.load_and_preprocess_csv(file_dir)



""" CREATE MASTER TABLE """
MasterTable = copy.deepcopy(people_table)
# We only keep a few of them
MasterTable = MasterTable[MasterTable.index < 1]

""" ADD THE TABLE 1 """

CVlib.add_to_whole_table(MasterTable,people_table, origins)

""" ADD THE TABLE 2 """
print "#######################"
file_dir = "./data/EBEC15.csv"
people_table = CVlib.load_and_preprocess_csv(file_dir)
CVlib.add_to_whole_table(MasterTable,people_table, origins)


""" ADD THE TABLE 3 """
print "#######################"
file_dir = "./data/TD14.csv"

people_table = CVlib.load_and_preprocess_csv(file_dir)
CVlib.add_to_whole_table(MasterTable,people_table, origins)

MasterTable_np = np.array(MasterTable)
MasterTable_list = MasterTable_np.tolist()

""" ADD THE TABLE 4 """
print "#######################"
file_dir = "./data/BESTIES.csv"

people_table = CVlib.load_dataset(file_dir)
CVlib.add_to_whole_table(MasterTable,people_table, origins)

MasterTable_np = np.array(MasterTable)
MasterTable_list = MasterTable_np.tolist()


""" LOAD PDFs """

people_names = MasterTable["full_name"].tolist()
people_name_pdfs = CVlib.get_CVpdf_name_table(MasterTable)

folder_in = "./CVs_brutos"
folder_out = "./CVs_ordenados"


found_flags = CVpdf.rename_CV_files_format1(folder_in,folder_out, people_names,people_name_pdfs)
print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"

indexes = np.where(found_flags[:,0] == 0)[0].tolist()
people_names = (np.array(people_names)[indexes]).tolist()
people_name_pdfs = (np.array(people_name_pdfs)[indexes]).tolist()

found_flags = CVpdf.rename_CV_files(folder_in,folder_out, people_names,people_name_pdfs)
indexes = np.where(found_flags[:,0] == 0)[0].tolist()
people_names = (np.array(people_names)[indexes]).tolist()
people_name_pdfs = (np.array(people_name_pdfs)[indexes]).tolist()

MasterTable.to_csv("Pene.csv", sep=',')

# Transform all the nan into 
## Transformar en putas listas pork pandas es puta mierda !!!!!!!!

## Elininate the column names
#del people [0]
#Npeople = Npeople -1
#
## Eliminate fucking duplicates
#
#deleteme = []
#for i in range (Npeople):
#    for j in range (Npeople):
#        if (i != j):
#            if (people[i][1] == people[j][1]):
#                if (people[i][2] == people[j][2]):
#                    deleteme.append(i)
#                    print people[i][1]
#                    people[i][1] = "pene"
#
#""" PUTA VIDA QUE SQL NO TOMA ACENTITOS, los muestra pero para el son lo mismo con que sin, para python no """
#
#deleteme = sorted(deleteme, reverse = True)
#for index in deleteme:
#    del people[index]
#
#Npeople = Npeople - len(deleteme)
#""" Que empiece el juego """ 
#
## Now we create a file in SQL format to introduce the people into the DataBase
#text_file = open("./insert_people.sql", "w")
#
## First line to say what we insert
#insert_line = "insert into people (" 
#for j in range(Ncol):
#    insert_line += column_names[j] 
#    if (j < Ncol - 1):
#        insert_line += ","
#insert_line += ") values \n"
#
## Last update line:
#
#Update_line = "ON DUPLICATE KEY UPDATE \n"
#
#text_file.write(insert_line);
#for j in range(Ncol):
#    Update_line += "\t" + column_names[j] + " = VALUES (" + column_names[j] + ")"
#    if (j < Ncol - 1):
#        Update_line += ",\n"
#        
#Update_line += " \n;\n"
#
#for i in range(Npeople):
#    text_file.write("\t(")
#
#    for j in range (Ncol):
#        content = people[i][j]
#        if (content != "NULL"):
#            text_file.write("\""+str(content)+"\"")
#        else:
#            text_file.write("NULL")
#            
#        if (j != Ncol -1 ):
#            text_file.write(",")
#        
#    text_file.write(")")
#    
#    if (i != Npeople -1 ):
#        text_file.write(",")
#    else:
#        text_file.write("\n")
#    
#    text_file.write("\n")
#    
#text_file.write(Update_line)
#
#text_file.close()
#
#
## """ RENAME FUCKING FILES """"
#
#
## Get the names 
#names_list = []












## Get the columns names and the indexes of rows
#rows = people_table.index.values.tolist()   # Indexes of rows
#cols = people_table.columns.values.tolist()
##print people_table[cols[0]][rows[0]]
#
## Transform to numpy and 
#people_table_np = np.array(people_table)
#people_table_list = people_table_np.tolist()
    

