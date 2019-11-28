 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 9:45:02 2019

@author: camillelamy


"""
import os
import re
import pandas as pd
import yaml

"""
###########

Add in data folder a folder named "df" and create df_articles.csv in df folder

############
"""

mon_dictionnaire = {}
df_articles = pd.DataFrame()

a = 1
b = 7290
for i in range (a,b):
    with open(os.getcwd()+"/data/articles_7250/article_%s.txt"%i, "r") as article:
        data = article.read()  
         
    
    data_dict = yaml.load(data, Loader=yaml.FullLoader)
    

    try :
        content_raw = data_dict.get("CONTENT")
        content_raw = content_raw.lower()
        content_raw = re.sub(r"\W"," ",content_raw)
        content_raw = re.sub(r"copyright abstract keywords introduction|copyright abstract keywords"," ",content_raw)
        content_raw = re.sub(r"  "," ",content_raw)
        content_raw = re.sub(r","," ",content_raw)
        content_raw = re.sub(r"\d"," ",content_raw)
        
        
    except :
        content_raw = "none"
        
    try : 
        title_raw = data_dict.get("TITLE")
        title_raw = re.sub(r","," ",title_raw)
    except :
        title_raw = "none"
        
    try : 
        kw_raw = data_dict.get("KEYWORDS")
        kw_raw = str (kw_raw)
        kw_raw = re.sub(r"\[|\]|\'|\,"," ",kw_raw)
    except :
        kw_raw = "none"
        
    try : 
        DOI_raw = data_dict.get("DOI")
        DOI_raw = re.sub(r","," ",DOI_raw)
        
    except:
        DOI_raw = "none"
        
    try : 
        ISSN_raw = data_dict.get("ISSN")
        ISSN_raw = re.sub(r","," ",ISSN_raw)
    except:
        ISSN_raw = "none"
        
    try:
        abstract_raw = data_dict.get("ABSTRACT")
        abstract_raw = abstract_raw.lower()
        abstract_raw = re.sub(r"\W"," ",abstract_raw)
        abstract_raw = re.sub(r"\d"," ",abstract_raw)
        abstract_raw = re.sub(r"\n"," ",abstract_raw)
        abstract_raw = re.sub(r"^abstract"," ",abstract_raw)
        
    except :
        abstract_raw = "none"     

    dict_data= {"1_DOI" : DOI_raw,
            "2_ISSN" : ISSN_raw,
            "3_TITLE" : title_raw, 
            "5_ABSTRACT" : abstract_raw,
            "6_CONTENT" : content_raw,
            "4_KEYWORDS" : kw_raw
            }
    
    df_articles = df_articles.append(dict_data, ignore_index=True)
    #print (int((i/b)*100),"%")
print (df_articles)
df_articles.to_csv(r'data/df/df_articles.csv')