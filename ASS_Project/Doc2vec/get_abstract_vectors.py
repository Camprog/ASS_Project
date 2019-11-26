#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:08:32 2019

@author: camillelamy
"""

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
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 


dictionnary = {}
dicti = {}
list_v = []
list_title = []
list_content = []
list_title_v = []

ps = PorterStemmer() 
content_stem = []

stop_words = set(stopwords.words('english'))

for i in range (1,1100):
    with open(os.getcwd()+"/Test_NLP/articles_6500_copie/article_%s.txt"%i, "r") as article:
         data = article.read()    
    
    data_dict = yaml.load(data, Loader=yaml.FullLoader)
    
    try :
        content_raw = str(data_dict.get("CONTENT"))
        print (type(content_raw))
        title_raw = data_dict.get("TITLE")
    except :
        content_raw = str("AZERTY")
        title_raw = "No_title"
    i += 1    
    content_raw = content_raw.lower()
    content_raw = re.sub(r"abstract","",content_raw)
    content_raw = re.sub(r"\d"," ",content_raw)
    content_raw = re.sub(r" (\w )*"," ",content_raw )
    content_raw = re.sub(r" (\w )*"," ",content_raw )
    content_raw = re.sub(r"db"," ",content_raw )
    content_raw = re.sub(r"(main|mainpdf|gif|png|jpg|jpeg|sml|pdf|docx|doc|item)"," ",content_raw)
    
    
    
    words = content_raw.split() 
    content_Filtered_t = []
    for w in words:
        if w not in stop_words:
            content_Filtered_t.append(w)
     
    content_Filtered = " ".join(content_Filtered_t)
  
    words_stem = word_tokenize(content_Filtered)
    
    for w in words_stem: 
        ww= ps.stem(w)
        content_stem.append(ww)
    

    content_stem_f = " ".join(content_stem)
    content_stem_f = re.sub(r","," ",content_stem_f)
    content_stem_f = re.sub(r"  "," ",content_stem_f)
    
    print (content_stem_f)
    
    
    list_content.append(content_stem_f)
    list_title.append(title_raw)
    

"""
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(list(list_content))]

model = Doc2Vec(documents, size=25, window=2, min_count=1, workers=4)

X=[]


for i in range(99):
    X.append(model.docvecs[i])
    liste_vecteur = list(model.docvecs[i])
    list_v.append(liste_vecteur)



title_v = zip(list_title,list_v)
list_title_v = list(title_v)


   
#print (list_title_v)    
#print ("Liste des vecteurs\n",list_v)

#export_data = zip_longest(*liste_v, fillvalue = ',')
    
with open(os.getcwd()+"/Test_NLP/title_Vecteurs_stem_content_v2.csv", 'w', encoding="UTF8", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow("v")
      wr.writerows(list_title_v)
"""