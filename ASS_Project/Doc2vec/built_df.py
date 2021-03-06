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
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import json
import csv
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize

from ass_constant import DOI_TAG as DOI
from ass_constant import ISSN_TAG as ISSN
from ass_constant import TITLE_TAG as TITLE
from ass_constant import ABSTRACT_TAG as ABSTRACT
from ass_constant import CONTENT_TAG as CONTENT
from ass_constant import KEYWORD_TAG as KEYWORD

"""
###########

Add in data folder a folder named "df" and create df_articles.csv in df folder

############
"""

stop_words = set(stopwords.words('english'))

mon_dictionnaire = {}
df_articles = pd.DataFrame()

a = 2000
b = 7000
for i in range(a, b):
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
        content_raw = re.sub(r"( \w\w )|( \w )"," ",content_raw)
        content_raw = re.sub(r"( \w\w )|( \w )"," ",content_raw)
        content_raw = re.sub(r"( \w\w )|( \w )"," ",content_raw)
        
        
        
        words = content_raw.split() 
        content_filtered = []
        for w in words:
            if w not in stop_words:
                content_filtered.append(w)
     
        content_raw = " ".join(content_filtered)
        
        
        #print(type(content_raw))
        #print (content_raw)
        
        
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
        kw_raw = re.sub(r"\[|\]|\'|\,|\;"," ",kw_raw)
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
        abstract_raw = re.sub(r"( \w\w )|( \w )"," ",abstract_raw)
        abstract_raw = str(abstract_raw)
        
        words_a = abstract_raw.split() 
        content_filtered_a = []
        for w in words_a:
            if w not in stop_words:
                content_filtered_a.append(w)
     
        abstract_raw = " ".join(content_filtered_a)
        
    except :
        abstract_raw = "none"     

    dict_data = {DOI: DOI_raw,
                 ISSN: ISSN_raw,
                 TITLE: title_raw,
                 ABSTRACT: abstract_raw,
                 CONTENT: content_raw,
                 KEYWORD: kw_raw
                 }
    
    df_articles = df_articles.append(dict_data, ignore_index=True)
    print((i/b)*100, "%")
print(df_articles)
df_articles.to_csv(r'data/df/df_articles_9.csv')
