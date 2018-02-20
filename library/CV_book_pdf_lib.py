from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import shutil
import lib_CV_Book as CVlib
import numpy as np

def getPDFContent(path = "../../../P3.pdf"):
    content = ""
    # Load PDF into pyPDF
    input_file = file(path, "rb")
    pdf = PdfFileReader(input_file)
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
        
    # Collapse whitespace
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    input_file.close()
    
    return content

import os
def rename_CV_files(folder_in, folder_out, table, remove_F = 0):
    # This function search a name into the pdfs of a folder and if it finds
    # one of the pdfs with that name, then it creates a copy of that file
    # with that name    
    # For every file it looks for a list of names
    # os.walk will help us walking through the directories.
    
    
    # Make sure the pdfs are asociated
#    CVlib.set_table_pdf_existance(folder_in, table)
    
    # First get only the people that has not already have an associated pdf
    people_nopdf = table[table["pdf_exists"] != True]
    
#    print people_nopdf.shape
    
    name_list = people_nopdf["full_name"].tolist()
    name_pdfs = CVlib.get_CVpdf_name_table(people_nopdf)
    indexes_list = people_nopdf.index.tolist()
    
    found_flags = np.zeros((len(name_list),1))
    
    for dirName, subdirList, fileList in os.walk(folder_in):  # FOR EVERY DOCUMENT
        # For every folder, going top - down
#        print('Found directory: %s' % dirName)
        # For every file in the document (
    
        for fname in fileList:

            # Read the file
            path = dirName + '/' + fname;
#            print path
            try:
                content = getPDFContent(path)
                
            except:
                print fname + " no se puede leer  !!!"
                content = ""
                continue
            
            # Standarize name and content
            content = content.lower()
            content = CVlib.remove_accents(str(content))
            
            for i in range(len(name_list)):     # FOR EVERY NAME
                name = name_list[i]
                name_st = name.lower()
                name_st = CVlib.remove_accents(name_st)

                pene1 = content.find(name_st)
        
                # A veces ponen el puto nombre como Montoya Catala, Manuel
                parts = name_st.split(" ")
                good_name = ""
                for part in parts[1:]:
                    good_name += part + " "
                good_name = good_name[:-1]
                good_name += ", " + parts[0]
                
                pene2 = content.find(good_name)

                if ((pene1 > -1)|(pene2 > -1)):  # If there is a matching
                    if (found_flags[i] == 1):
                        print name_pdfs[i] + " already found XXXX "
                        
                    found_flags[i] = 1
                    ###############################################
                    ######## Change the status of table ###########
                    ###############################################
                    table["pdf_exists"][indexes_list[i]] = True
#                    print table["pdf_exists"][indexes_list[i]]
                    shutil.copy2(path, folder_out + "/" + name_pdfs[i])
                    
                    if (remove_F == 1):  # If we want to remove the file
                        os.remove(path)
                        
                    print "FOUND MATCH: " + name + " -> " + fname
                    break
    return found_flags
    
def rename_CV_files_format1(folder_in, folder_out, table, remove_F = 0):
    # This function search a name into the pdfs of a folder and if it finds
    # one of the pdfs with that name, then it creates a copy of that file
    # with that name    
    # For every file it looks for a list of names
    # os.walk will help us walking through the directories.
    
    
    # Make sure the pdfs are asociated
#    CVlib.set_table_pdf_existance(folder_in, table)
    
    # First get only the people that has not already have an associated pdf
    people_nopdf = table[table["pdf_exists"] != True]

    name_list = people_nopdf["full_name"].tolist()
    name_pdfs = CVlib.get_CVpdf_name_table(people_nopdf)
    indexes_list = people_nopdf.index.tolist()
    found_flags = np.zeros((len(name_list),1))
    
    for dirName, subdirList, fileList in os.walk(folder_in):  # FOR EVERY DOCUMENT
        # For every folder, going top - down
#        print('Found directory: %s' % dirName)
        # For every file in the document (
        for fname in fileList:
            path = dirName + '/' + fname;
#            print path
            
            # We expect to finf the name in format 004-Antonio_Relano_OR.pdf
#            name_pdf = fname.split("-")[1]
            name_pdf = fname.split("_")
            
            name_pdf = name_pdf[:-1]
#            if ((name_pdf[-1] == "AP.pdf")|
#                (name_pdf[-1] == "CS.pdf")|
#                (name_pdf[-1] == "OR.pdf")|
#                (name_pdf[-1] == "TD.pdf")):
#                    name_pdf = name_pdf[:-1]
#                    
#            if ((name_pdf[-1] == "E14")|
#                (name_pdf[-1] == "E13")|
#                (name_pdf[-1] == "E12")|
#                (name_pdf[-1] == "ES14")|
#                (name_pdf[-1] == "ES13")|
#                (name_pdf[-1] == "ES12")) :
#                    name_pdf = name_pdf[:-1]
#            print name_pdf
            
            good_name = ""
            for part in name_pdf:
                good_name += part + " "
            name_pdf = good_name[:-1]
            

            for i in range(len(name_list)):     # FOR EVERY NAME
                name = name_list[i]
                
                good_name = name
                
                namespt = name.split(" ")
                
                if (len(namespt) > 2):  # MAYBE IN THE FILES EL SEGUNDO APELLIDO NO SE PUSO
                    
                    good_name = namespt[0] + " " + namespt[1]

#                    print good_name
                    
                name1 = CVlib.remove_accents(good_name).lower()
                name2 = CVlib.remove_accents(name_pdf).lower()
        
                    
                if ( name1 == name2 ):  # If there is a matching
                
                    if (found_flags[i] == 1):
                        print name_pdfs[i] + " already found XXXX "
                    
                    found_flags[i] = 1
                    ###############################################
                    ######## Change the status of table ###########
                    ###############################################
                    table["pdf_exists"][indexes_list[i]] = True
                    shutil.copy2(path, folder_out + "/" + name_pdfs[i])
                    
                    if (remove_F == 1):  # If we want to remove the file
                        os.remove(path)
                        
                    print "FOUND MATCH: " + name + " -> " + fname
                    
                    break
#            else:
#                print "NOT FOUND MATCH: " + name
    return found_flags
                

import pandas as pd
def download_pdfs_table (table_CV, folder_out):
    # Tries to download all the CV.
    # Requires the file to have the column "pdfurl"

    # Create empty list for not downloaded
    NotDownloadedTable = pd.DataFrame(columns = ["full_name","birthday","pdfurl","pdfname"])

    # Obtain index of people 
    people_ind = table_CV.index.values
    Nu = len(people_ind) 
    
    for i in range(Nu):   # For every person to download its CV
        person = table_CV.ix[i]
        
        # First we check if we already downloaded it and name it.
        file_exists = CVlib.check_CVpdf_noindex(folder_out,person)
        if (file_exists == True):
            print person["full_name"] + " Already donwloaded and named"
            
        else:
            name_pdf = CVlib.get_CVpdf_name_noindex(table_CV.ix[i])  # Get the name to be downloaded
            url = table_CV["pdfurl"][i]
            
    #        time.sleep(5)  # Wait a second so that maybe the system does not see us as bots
            success = download_pdf(url ,folder_out,name_pdf)
            
            if (success == 0): # If we failed to download the file
                print person["full_name"] + " couldn't be downloaded"
                person_data = person[["full_name","birthday","pdfurl"]]
                person_data["pdfname"] = name_pdf
                CVlib.append_person(NotDownloadedTable,person_data)

    return NotDownloadedTable



import urllib2                                                # needed for functions,classed for opening urls.

def download_pdf (url,folder,file_name):
    
    url = url.replace(" ","%20")    

    try:
        usock = urllib2.urlopen(url)                                  #function for opening desired url
        
    except urllib2.HTTPError, e:
#        print e.fp.read()
#        print "Este pdf no se puede descardar"
        return 0
    
    # check that the file is in .pdf
    extension =  url.split(".")[-1]
    
    if (extension != "pdf"):
        file_name =  file_name[:-3] + extension
    
    f = open(folder + file_name, 'wb')                                     #opening file for write and that too in binary mode.
    file_size = int(usock.info().getheaders("Content-Length")[0]) #getting size in bytes of file(pdf,mp3...)
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
     
    downloaded = 0
    block_size = 8192                                            #bytes to be downloaded in each loop till file pointer does not return eof
    while True:
       buff = usock.read(block_size)
       if not buff:                                             #file pointer reached the eof
           break
     
       downloaded = downloaded + len(buff)
       f.write(buff)
       
#       download_status = r"%3.2f%%" % (downloaded * 100.00 / file_size) #Simple mathematics
#       download_status = download_status + (len(download_status)+1) * chr(8)
#       print download_status,"done"
    print "Dowloaded"
    f.close()
    return 1