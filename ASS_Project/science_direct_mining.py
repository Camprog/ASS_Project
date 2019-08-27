#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:44:26 2019

@author: camillelamy
"""


from elsapy.elsclient import ElsClient

import json
import re

from article_scrap.ass_article import ScienceDirectArticle

import os
from pathlib import Path
#import random

import logging

#logging.basicConfig(level=logging.INFO)

    
## Load configuration
con_file = open(os.getcwd()+"/article_scrap/config.json")
config = json.load(con_file)
con_file.close()
client = ElsClient(config['apikey'])

##ScienceDirect (full-text) document example using PII

#================================
with open(os.getcwd()+"/data/article_list/list_pii_EM.json") as json_file:
    pii_code_EM = json.load(json_file)
 
with open(os.getcwd()+"/data/article_list/list_pii_RTM.json") as json_file:
    pii_code_RTM = json.load(json_file)
    
with open(os.getcwd()+"/data/article_list/list_a.json") as json_file:
    code_PII = json.load(json_file)

list_PII_RTM = re.sub( "[^\w]", " ",  pii_code_RTM).split()
print("Research transport part B :",len(list_PII_RTM))
list_PII_EM = re.sub("[^\w]", " ",  pii_code_EM).split()
print("Ecological modeling :",len(list_PII_EM))
list_PII = list_PII_RTM + list_PII_EM
#=================================

"""
# IF THE CODE BREACKDOWN, uncomment the code below and commented on the code above (between #====)
#=================================
with open(os.getcwd()+"/data/article_list/list_a.json") as json_file:
    code_PII = json.load(json_file)
    
list_PII = re.sub("[^\w]", " ", code_PII).split()
print("Liste total PII : ",len(list_PII))
#=================================
"""
#r=5
#list_rdm = random.sample(List_PII,r) + random.sample(List_PII_RTM,r)
#list_rdm = ["S0191261510000378"]
#print ("PII list : ",list_rdm)


def JsonList(y) :
#    
    List = json.dumps(y)
    with open(os.getcwd()+"/data/article_list/list_a.json",'w') as outfile:  
        json.dump(List,outfile)

def test_get_articles(i,list):   
    
    for i in list:
        print (len(list_PII))
        logging.debug("Phase 1")
        ass_doc = ScienceDirectArticle(i, client)
        
        if ass_doc.is_undesired():
            logging.warning("Filtred document => meaningless")
            list_PII.remove(i)
            JsonList(list_PII)
            continue
        if ass_doc.author_1() is False:
            logging.warning("Filtred document => author error")
            list_PII.remove(i)
            JsonList(list_PII)
            continue
        else:
        #print (ass_doc.doi())
            logging.debug("Phase 2")
            doss = Path(os.getcwd()+"/data/articles/")
            res_file = str(doss)+"/SD_article_"+(ass_doc.doi())+".txt"
            logging.debug("Phase  4")
            ass_doc.save(res_file)
            logging.info("OK \n")
            print (len(list_PII))
            list_PII.remove(i)
            JsonList(list_PII)

x= int   
articles = test_get_articles(x,list_PII)  
logging.info(articles)
    

