#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:33:17 2019

@author: camillelamy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 18:45:02 2019

@author: camillelamy


"""
import os
import re
import yaml
import json
import pandas as pd
import csv
import nltk
import nltk
import io 
import nltk.corpus
from itertools import zip_longest
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import json
import csv


dictionnary = {}
dicti = {}
liste_v = []
list_title = []
list_content = []

stop_words = set(stopwords.words('english'))

for i in range (1,10):
    with open(os.getcwd()+"/Test_NLP/articles_6500_copie/article_%s.txt"%i, "r") as article:
         data = article.read()    
    
    data_dict = yaml.load(data, Loader=yaml.FullLoader)
    #if type(data_dict.get("CONTENT")) 
    try :
        content_raw =data_dict.get("CONTENT")
    except :
        content_raw = "AZERTY"
        
    content_raw = content_raw.lower()
    #abstract_filtred = [word for word in abstract if word not in stopwords.words('english')]
    #print(abstract_filtred)
    #content_raw = re.sub(r"Abstract","",content_raw)
    content_raw = re.sub(r" (\w )*"," ",content_raw )
    content_raw = re.sub(r"db"," ",content_raw )
    
    words = content_raw.split() 
    #print (words)
    content_Filtered_t = []
    for w in words:
        if w not in stop_words:
            content_Filtered_t.append(w)
    
    #print(abstract_Filtered_t)
    content_Filtered = " ".join(content_Filtered_t)
    #print (content_raw)
    print (content_Filtered)
    
    list_content.append(content_Filtered)
    




documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(list(list_content))]

model = Doc2Vec(documents, size=25, window=2, min_count=1, workers=4)

X=[]

for i in range(9):
    X.append(model.docvecs[i])
    liste_vecteur = list(model.docvecs[i])
    liste_v.append(liste_vecteur)
    
    
print ("Liste des vecteurs\n",liste_v)

#export_data = zip_longest(*liste_v, fillvalue = ',')
    
with open(os.getcwd()+"/Test_NLP/Vecteurs_titl.csv", 'w', encoding="UTF8", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow("v")
      wr.writerows(liste_v)
  
#print ("Title: ",title,"\n\nAbstract: ", abstract,"\n\n")

#print(pd.read_csv("Vecteurs.csv"))  




#list_content
#liste_vecteur
# 
#my = json.dumps(list_content)
#
#mylist_content = JSON.stringify(list_content)
#localStorage.setItem("testJSON", mylist_content)


#liste_Content_Vecteur = zip(list_content,liste_vecteur)
#print (liste_Content_Vecteur)
#    
#   
    
"""    
    export_data = zip_longest(*list_ta, fillvalue = '/')
    
    with open(os.getcwd()+"/Test_NLP/art_titl_abst.csv", 'w', encoding="UTF8", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("Abstract","Title"))
      wr.writerows(export_data)
  
    print ("Title: ",title,"\n\nAbstract: ", abstract,"\n\n")

print(pd.read_csv("art_titl_abst.csv"))
"""


