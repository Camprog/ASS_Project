#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 09:35:01 2019

@author: camillelamy
"""
import os
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument



 
list_v = []
df = pd.read_csv(os.getcwd()+"/data/df/df_articles_9.csv")

list_content = df['6_CONTENT'].tolist()
print (len(list_content))


documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(list_content)]

model = Doc2Vec(documents, vector_size=25, window=2, min_count=1, workers=4)

X=[]
print("phase_3")

for i in range(len(list_content)):
    try:
        X.append(model.docvecs[i])
        liste_vecteur = list(model.docvecs[i])
        list_v.append(liste_vecteur)
        #print (i,"vectors")
    except:
        list_v.append(list("none"))
        #print(i, "errors")
        continue


df['7_VECTORS'] = list_v  
df.to_csv(r'data/df/df_articles_vecteur_content_2.csv') 
print(list_v)


    
#print ("Longueur liste",len(list_kw),len(list_v))
#list_kw_v = zip(list_kw,list_v)


#title_v = zip(list_title,list_v)
#list_title_v = list(title_v)


   
#print (list_title_v)    
#print ("Liste des vecteurs\n",list_v)

#export_data = zip_longest(*liste_v, fillvalue = ',')
    
#with open(os.getcwd()+"/Test_NLP/Vecteurs.csv", 'w', encoding="UTF8", newline='') as myfile:
#      wr = csv.writer(myfile)
#      wr.writerow("v")
#      wr.writerows(list_kw_v)