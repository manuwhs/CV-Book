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

table_columns = [
                "full_name",    # Full name of the person
                "origin",       # Event from which we got his CV
                "birthday",     # Date of birth of the person
                "email",        # Email of the person
                "phone",        # Phone number of the person
                "current_studies",       # Degree or Master the person is studying
                "start_year",            # Year the person started his studies.
                "pdf_exists"]   # Yes or No. It tells if there exists a pdf assoicated with it

# Possible origins                
origins = [
	["EBEC13", 2013],
	["TD14", 2014],
	["SC14", 2014],
	["EBEC14", 2014],
	["TD15", 2015],
	["EBEC15", 2015],
	["BESTIE", 9999]   # BESTies al poder
 ]
 
origins = np.array(origins).T.tolist()
 
# Possible Studies      

education =  [
 	 "Grado en Ingeniería Biomédica" ,
	 "Grado en Ingeniería en Tecnologías de Telecomunicación" ,
	 "Grado en Ingeniería en Tecnologías Industriales" ,
	 "Grado en Ingeniería Mecánica" ,
	 "Grado en Ingeniería Aeroespacial" ,
	 "Grado en Ingeniería Electrónica Industrial y Automática" ,
	 "Grado en Ingeniería Informática" ,
	 "Grado en Ingeniería de la Energía" ,
	 "Grado de Ingeniería de Sistemas Audiovisuales" ,
	 "Grado en Ingeniería de Sistemas de Comunicaciones" ,
	 "Grado en Ingeniería Telemática" ,
     "Grado en Ingeniería Eléctrica" ,
	 "Doble grado en Ingeniería Informática y Administración de Empresas" ,

	 "Máster en Ingeniería Industrial" ,
	 "Máster en Métodos Analíticos para Datos Masivos: Big Data" ,		
	 "Máster en Ciberseguridad" ,		
	 "Máster en Energías Renovables en Sistemas Eléctricos" ,			
	 "Máster en Gestión y Desarrollo de Tecnologías Biomédicas",		
	 "Máster en Ingeniería Informática" ,		
	 "Máster en Ingeniería de Máquinas y Transportes" ,
	 "Máster en Ciencia e Ingeniería de Materiales" ,		
	 "Máster en Física de Plasmas y Fusión Nuclear" ,		
	 "Máster en Ingeniería de Sistemas Electrónicos y Aplicaciones" ,		
	 "Máster en Ingeniería Matemática" ,
	 "Máster en Matemática Industrial" ,
	 "Máster en Mecánica Industrial" ,	
	 "Máster en Multimedia y Comunicaciones" ,		
	 "Máster en Ciencia y Tecnología Informática" ,	
	 "Máster en Robótica y Automatización" ,		
	 "Máster en Ingeniería Telemática" ,		

	 "Ingeniería Superior" ,
	 "Ingeniería Superior Industrial" ,
	 "Ingeniería Superior de Telecomunicaciones" ,
	 "Otros" 
  ]


laguaje_levels = [ 
                	["None", 0],
                	["A1", 1],
                	["A2", 2],
                
                	["B1", 3],
                	["B2", 4],
                
                	["C1", 5],
                	["C2", 6],
                
                	["Nativo",7]
                 ]

dictionaries = {
                "table_columns": table_columns,
                "origins": origins,
                "education":education
                }

MasterTable = pd.DataFrame(columns = table_columns)

fo.save_MasterTable(MasterTable,dictionaries)
