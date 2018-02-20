# -*- coding: utf-8 -*-
"""
u
"""
# We use pandas library to read CSV data.
import pandas as pd
import numpy as np
import unicodedata
import os
import shutil

### LOADING FUNCTIONS ###
def load_dataset(file_dir = "./dataprices.csv"):
    
    data = pd.read_csv(file_dir, sep = ',') # header = None, names = None  dtype = {'phone':int}
    Nsamples, Ndim = data.shape   # Get the number of bits and attr

    return data
    
def load_and_preprocess_csv(file_dir):
    people_table = load_dataset(file_dir)
    Npeople, Ncol = people_table.shape
    
    # If there is an empty row, pandas reads it as a Nan, we want to change it
    replance_NaN_NULL(people_table)
    
    # Transform float to int coz pandas reads float as default
    people_table["phone"] = people_table["phone"].astype(int)
    people_table["start_year"] = people_table["start_year"].astype(int)
    
    normalize_birthday(people_table)
    normalize_full_names(people_table)
    return people_table

### DATA PREPROCESSING FUNCTIONS 

def replance_NaN_NULL (table):
    # Replaces the empty values for NULL or -1
    rows = table.index.values   # Indexes of rows
    cols = table.columns.values

    for i in cols:
        for j in rows:
            content = table[i][j]
            if (isinstance(content,str) == False):
                if (np.isnan(content) == True):
                
                    if ((i == "phone")|(i == "start_year")):
                        table[i][j] = -1
                    else:
                        table[i][j] = "NULL"

def normalize_birthday (table):
    # Makes all the birthdays to be in the format DD/MM/YYYY
    rows = table.index.values   # Indexes of people
#    print rows
    for j in rows:    # For every person
#        print j
        bday = table["birthday"][j]

        if (bday != "NULL"):   # If we dont have a birthday

            bday = bday.replace('-','/')    # In case it is separated by "-"
#            print bday
            bday = bday.split("/")  # Now bday should have bday[0] = day, bday[1] = month, bday[2] = year
            
            if (len(bday) == 3):    # If the date given is not in an expected format
       
                # We add the 0 at left if it does not exist
                if (len(bday[0]) == 1):
                    bday[0] = "0" + bday[0]
                    
                if (len(bday[1]) == 1):
                    bday[1] = "0" + bday[1]
                
                # If we are given the year as 92, 94...
                if (len(bday[2]) == 2):   
                    if (int(bday[2])<50):
                        bday[2] = "20" + bday[2]
                    else:
                        bday[2] = "19" + bday[2]
                
                good_bday = bday[0] + "/" + bday[1] + "/" + bday[2] 
                table["birthday"][j] = good_bday
            else:
                table["birthday"][j] = "NULL"
#                print good_bday


def remove_all_shit_spaces(table, column):
    rows = table.index.values   # Indexes of people
    for j in rows:    # For every person
        name = table[column][j]
        name = name.lower()
        name = name.split(" ")  # Divide in words
        Nspaces = name.count("")
        
        for i in range(Nspaces):
            name.remove("")
        
        good_name = ""
        for parts in name:
            good_name += parts + " "
        
        good_name = good_name[:-1]  # Delete las " "
        table[column][j] = good_name
        
def normalize_full_names(table):
    # At least make sure all names are lower case exept the fisrt letter 
    # of every word exept "el", "la

    rows = table.index.values   # Indexes of people
    no_upper_words = ["el","la","los","las","de","del"]
    
    for j in rows:    # For every person
        name = table["full_name"][j]
        name = name.lower()
        name = name.split(" ")  # Divide in words
        
        """ Some pople put 2 " " or " " at the end, we have to kill that """
        Nparts = len(name)
        
        for i in range (Nparts):
            if (name[i] == ''):
                print "Name " + table["full_name"][j] + " has spaces where it shouldnt"
                print "Index = " + j
                # We are gonna remove them
 
        Nparts = len(name)
        for i in range (Nparts):
            try:
                indx = no_upper_words.index(name[i])
            except ValueError:
                indx = -1

            if (indx == -1):
                if (len(name[i]) > 1):
                    name[i] = name[i][0].upper() +  name[i][1:]
                else:
                    name[i] = name[i].upper()
        good_name = ""
        for parts in name:
            good_name += parts + " "
        
        good_name = good_name[:-1]  # Delete las " "
        table["full_name"][j] = good_name
#        print good_name

def remove_accents(input_str):

    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str, 'utf8'))
    
    ret_u = u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
    return str(ret_u)

def normalize_text(input_str):
    noacc = remove_accents(input_str)
    noacc = noacc.lower()
    return noacc
    
#### ADDING FUNCTIONS
def add_to_whole_table (MasterTable, table, origins):
    # This functions adds to the Master Table the table given
    new_rows = table.index.values
    
    Nnew = new_rows.size
    for i in range(Nnew):  # For every new person in the table
        add_person (MasterTable, table.ix[i], origins)


def update_person (table, person, index):
    # Given a table, a person and an index of the table
    # this function updates the table with them 

    cols_p = person.index.tolist()  # Columns of the person
    index_p = index
    for j in cols_p: # Replace all the cols the new person has
        table[j][index_p] = person[j]
 
        
def add_person (table, person, origins):
    duplicate = check_unique(table,person)  # Check if there is another person
    
    if (duplicate > -1): # If there is a duplicate
        newer = check_newest(table.ix[duplicate],person,origins)
        print person["full_name"] + " duplicated"
        
        if (newer == 1):  # If we have to change the data
            print "Updated"
            update_person(table,person, duplicate)
    else:
        append_person(table, person)


def modify_person (table, person,origins):
    # This function assumes the person index is already
    # on the dataset and it allows to modify names also
    index = person.name
#    print index
    
    if (person["full_name"] == "Null"): # If the name of the person is set to NULL
        # It is Null because of the Name preprocessing
        remove_person(table, index)
        return -1
        
    name_mod = check_namebday_modified(table.ix[index], person)
    
    if (name_mod == 1):
        # If the name has been modified first we check 
        # if there is another person with that new name in the table
        unique = check_unique_weak(table, person)
        
        if (unique != -1): # if the new person already exists
            print "Modified name " + person["full_name"] + " already existed"
            print "Removing oldest one"
            newest = check_newest (table.ix[unique], person, origins)
            
            if (newest == 0):  # If the newest is the one already in the dataset
                remove_person(table, index)   # We remove the one we were modifing
                print "Modified one, index = " + str(index)
                return -1
                
            else:
                remove_person(table, unique)  # Remove the older one
                print "Removing the one that matches the modified one , index = " + str(unique) 
                
        modify_person_namebday(table, person)
        
    # Now that we have changed the file safely we change everything
    update_person (table, person, index)
    

def remove_person (table, index):
    # This function removes a person and

    table.drop(index, inplace = True)
    print "Index " + str(index) + " removed"

def modify_person_namebday (table, person):
    # This function modifies the name, bday and pdfname
    path = "./all_pdfs/"
    index = person.name
    
    print "Changing " + table.ix[index]["full_name"] +" by " + person["full_name"]
    
    # Now we change the file name and the name in the BBDD
    old_pdf_name = get_CVpdf_name(table.ix[index])
    new_pdf_name = get_CVpdf_name(person)
    
    try:
        print "Name and file changed"
        shutil.copy2(path + old_pdf_name, path + new_pdf_name)
        os.remove(path + old_pdf_name) 
    except:
        print "Already removed or file didnt existed"
    
    table["full_name"][index] = person["full_name"]
    table["birthday"][index] = person["birthday"]
    
def check_namebday_modified(person_old, person_new):
    # Checks if the name or bday has been modified
    name1 = remove_accents(person_old['full_name'])
    name2 = remove_accents(person_new['full_name'])
    if (name1 == name2):
        if (person_old['birthday'] == person_new['birthday']):
            return 0
    print "MODIFIED"
    return 1
                

def append_person (table, person):
    # Biggest next index
    if (len(table.index) > 0):
        next_indx = table.index.values[-1] + 1
    else:
        next_indx = 0
    table.loc[next_indx] = person   # Add person to the table
    
#### CHECKING FUNCTIONS      
def check_newest (person_i1, person_i2, origins):
    # We can check what is the newest introduction by means of the origin 
    origin_1 = person_i1["origin"]
    origin_2 = person_i2["origin"]
    
#    print origin_1
    
    date_1 = origins[1][origins[0].index(origin_1)]
    date_2 = origins[1][origins[0].index(origin_2)]
    
    if (date_2 >= date_1):
        return 1;
    return 0
    
def check_unique (table, person):
    # Checks if a person is unique in a table

    rows = table.index.values
#    print rows.size
    for i in rows:
        name1 = remove_accents(table['full_name'][i])
        name2 = remove_accents(person['full_name'])
        if (name1 == name2):
            if (table['birthday'][i] == person['birthday']):
                return i
    return -1

def check_unique_weak (table, person):
    # Checks if a person is unique in a table EXACTLY
    # This is done to be able to modify accents thourght he SS

    rows = table.index.values
#    print rows.size
    for i in rows:
        name1 = table['full_name'][i]
        name2 = person['full_name']
        if (name1 == name2):
            if (table['birthday'][i] == person['birthday']):
                return i
    return -1
    
def get_CVpdf_name(person):
    # Outputs the name of the pdf CV from a table entry.
    name = person["full_name"]
    bday = str(get_bday_int(person["birthday"]))
    index_p = person.name  # Index of the person in the MasterTable
    
    
    pdfname = name + "_"+ bday +"_" + str(index_p) + ".pdf"

    return pdfname

def get_CVpdf_name_table(table):
    # Outputs the name of the pdf CV from a table entry.
    rows = table.index.values
#    print rows.size
    pdfs_names = []
    
    for i in rows:
        pdfname = get_CVpdf_name(table.ix[i])
        pdfs_names.append(pdfname)
        
    return pdfs_names
    
def get_bday_int(bday_str):
    # Get an int YYYYMMDD from char DD/MM/YYYY
#    print bday_str
#    print bday_str
    if (bday_str == "NULL"):
        return 0
#    print bday_str
    parts = bday_str.split("/")
    
    bday_strpost = parts[2] + parts[1] + parts[0]
    
    return int(bday_strpost)


    
def check_CVpdf (folder, person):
    # It checks if there is the pdf file of the given person

    pdf_name =  get_CVpdf_name(person)
    exist = os.path.exists(folder + pdf_name)
    
    return exist

def check_CVpdf_noindex (folder, person):
    # It checks if there is the pdf file of the given person

    pdf_name =  get_CVpdf_name_noindex(person)
    exist = os.path.exists(folder + pdf_name)
    
    return exist
    
def set_table_pdf_existance(folder, table):
    
    rows = table.index.values
#    print rows.size
    pdfs_names = []
    
    for i in rows:
        person = table.ix[i]
        existance = check_CVpdf(folder, person)
        table["pdf_exists"][i] = existance
        
    return pdfs_names
    

def get_person_indx(table, full_name, birthday):
    subtable = table[table["full_name"] == full_name]
#    print subtable
    subtable = subtable[table["birthday"] == birthday]
    
    index = subtable.index.values.tolist()
    
    if (len(index) == 0):  # If there was nobody with that name
       return -1
       
    return index[0]
    
    
def get_person_indexes_from_pdfname(pdfname):
    # The pdfname has the convention Name-YYYYMMDD.pdf
#    print pdfname
    
    full_name = pdfname.split("_")[0]
    bday = pdfname.split("_")[1]
    
    if (bday == "0"):
        bday = "NULL"
    else:
        bday = str(bday[6:8]) + "/" + str(bday[4:6]) + "/" + str(bday[0:4])
    
    index = int(pdfname.split("_")[2].split(".")[0])
#    print full_name,bday
    
    return full_name,bday,index
    
def add_new_event(ds,event_name, event_time):
    if (ds["origins"][0].count(event_name) > 0): # If it already existed
        index = ds["origins"][0].index(event_name)
        ds["origins"][1][index] = event_time
        print "Event: " + event_name + " already exists"
    else:
        ds["origins"][0].append(event_name)
        ds["origins"][1].append(event_time)



#######################################################################
### This functions were to change the way files were named 

def rename_all_pdfs(path, table):

    indexes = table.index.tolist()
    for i in indexes:
        person = table.ix[i]
        old_name = get_CVpdf_name_old(person)
        new_name = get_CVpdf_name(person)
        
        print old_name, new_name
        
        try:
            shutil.copy2(path + old_name, path + new_name)
            os.remove(path + old_name) 
        except:
            print "Already removed"
        
def get_CVpdf_name_old(person):
    # Outputs the name of the pdf CV from a table entry.
    name = person["full_name"]
    bday = str(get_bday_int(person["birthday"]))
    
    pdfname = name + "-"+ bday + ".pdf"

    return pdfname
    
    
###########################################################################
### NO index version names for when we dont know the indexes
# For example when we download the files
    
def get_CVpdf_name_noindex(person):
    # Outputs the name of the pdf CV from a table entry.
    name = person["full_name"]
    bday = str(get_bday_int(person["birthday"]))
    pdfname = name + "_"+ bday + ".pdf"
    return pdfname

def get_person_namebday_from_pdfname(pdfname):
    # The pdfname has the convention Name-YYYYMMDD.pdf
#    print pdfname
    
    full_name = pdfname.split("_")[0]
    bday = pdfname.split("_")[1].split(".")[0]
    
    if (bday == "0"):
        bday = "NULL"
    else:
        bday = str(bday[6:8]) + "/" + str(bday[4:6]) + "/" + str(bday[0:4])
    

#    print full_name,bday
    
    return full_name,bday

