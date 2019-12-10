#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 12:22:25 2019

@author: camillelamy
"""

# import these modules 
#from nltk.stem import WordNetLemmatizer 
#  
#lemmatizer = WordNetLemmatizer() 
#  
#print("rocks :", lemmatizer.lemmatize("rocks")) 
#print("corpora :", lemmatizer.lemmatize("corpora")) 
#  
## a denotes adjective in "pos" 
#print("better :", lemmatizer.lemmatize("better", pos ="a")) 
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import os
import re
import pandas as pd
import yaml
import csv

"""
nltk.download('wordnet')
"""
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

list_lem = []
df = pd.read_csv(os.getcwd()+"/data/df/df_vecteur_revu.csv")

list_content = df['6_CONTENT'].tolist()

lemmatizer = WordNetLemmatizer()



for i in range(len(list_content)):
    
    sentence = list_content[i]
    new_sentence = " ".join([lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(sentence)])
    list_lem.append(new_sentence)
    print(round((len(list_lem)/len(list_content)*100),2),"%")
  

df['9_Content_lem_POSTAG'] = list_lem 
df.to_csv(r'data/df/df_vecteur_revu.csv')
