#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:44:26 2019

@author: camillelamy
"""


from elsapy.elsclient import ElsClient
#from elsapy.elsdoc import FullDoc
import json
import re
from ASS_Project.article_scrap.ass_article import ScienceDirectArticle
#from ASS_Project.article_scrap.jasss_scrap_util import concat_title
import os
from pathlib import Path
import random


    
## Load configuration
con_file = open(os.getcwd()+"/article_scrap/config.json")
config = json.load(con_file)
con_file.close()
client = ElsClient(config['apikey'])

#ScienceDirect (full-text) document example using PII

with open(os.getcwd()+"/../list_pii_EM.json") as json_file:
    pii_code = json.load(json_file)
 
with open(os.getcwd()+"/../list_pii_RTM.json") as json_file:
    pii_code_RTM = json.load(json_file)


List_PII_RTM = re.sub("[^\w]", " ",  pii_code_RTM).split()
print(len(List_PII_RTM))
List_PII = re.sub("[^\w]", " ",  pii_code).split()
print(len(List_PII))

r=500
list_rdm = random.sample(List_PII,r) + random.sample(List_PII_RTM,r)
#list_rdm = ["S0304380012004012"]
print ("PII list : ",list_rdm)


def test_get_articles(i,list):   
    for i in list:
        
        print("Phase 1")
        ass_doc = ScienceDirectArticle(i, client)
    
        if ass_doc.is_undesired():
            pass
        else:
        #print (ass_doc.doi())
            print("Phase 2")
            doss = Path(os.getcwd()+"/data/")
            print("Phase 3")
            res_file = str(doss)+"/SD_article_"+(ass_doc.doi())+".txt"
            print("Phase 4")
            ass_doc.save(res_file)
            print("Phase 5")
            
            ass_doc._sd_article.write()
            print("Phase 6 \n\n\n\n\n\n\n") 

x= int   
articles = test_get_articles(x,list_rdm)  
print (articles)
    


#    
#    
    
#titre_concat = concat_title(ass_doc.title)
#    print (titre_concat)
#    

    
    #for i in pii_doc.data["coredata"]["dcterms:subject"][i]["$"]:
        
#    for i in (pii_doc.data["coredata"]["dcterms:subject"][]["$"]):
    #for i in pii_doc.data["coredata"]["dcterms:subject"]:
       # for j in i:
       #     keyword = j[0]["$"]
       #     print(keyword)
        
        #keywords = (pii_doc.data["coredata"]["dcterms:subject"][i]["$"])
        #print (Keywords)
        


#    Abstract = pii_doc.data["coredata"]["dc:description"]
#    Revue = pii_doc.data["coredata"]["prism:publicationName"]
#    Text = pii_doc.data["originalText"]
#    
#    #print (pii_doc.title,Abstract, Revue)
#    Article = str(Revue)+str(pii_doc.title) + str(Abstract)+ str(Text)
#    print (Article)
#    
#    with open("/Users/camillelamy/Dossier_Python/ASS_Project/ASS_Project/article_scrap/data/"+str(re.sub(" ","_",pii_doc.title))+".txt",'w') as outfile:  
#        json.dump(Article, outfile)
    

 #   Abtract, keyword, Revue, Author and texte variable, go to searsh information in data folder. 
    
    
    

#Keywords = (pii_doc.data["coredata"]["dcterms:subject"][0]["$"],
            #pii_doc.data["coredata"]["dcterms:subject"][1]["$"])
            #pii_doc.data["coredata"]["dcterms:subject"][2]["$"],
            #pii_doc.data["coredata"]["dcterms:subject"][4]["$"],)


#Revue = pii_doc.data["coredata"]["prism:publicationName"]
#Author = (pii_doc.data["coredata"]["dc:creator"][0]["$"],
#         pii_doc.data["coredata"]["dc:creator"][1]["$"],
#          pii_doc.data["coredata"]["dc:creator"][2]["$"],)
          
#Text = pii_doc.data["originalText"]


#
#print ("Revue: \n\n ",Revue,"\n\n")
#print ("Keywords: \n\n ",Keywords,"\n\n")
#print ("Author:\n\n",Author,"\n\n")

#itérer pour Keyword et Author



#from elsapy.elsclient import ElsClient
#from JasssArticle import ScienceDirectArticle as SD_A
#import json
#import re
#from elsdoc import FullDoc
#
### Load configuration
#con_file = open("config.json")
#config = json.load(con_file)
#con_file.close()
#
### Initialize client
#client = ElsClient(config['apikey'])
#
#
#with open("list_pii_RTM.json") as json_file:  
#    pii_code = json.load(json_file)
#print ("Liste des codes PII :",pii_code)
#print (type(pii_code))
#
#
#List_PII = re.sub("[^\w]", " ",  pii_code).split()
#print ("List_PII",List_PII)
#print ("List_PII type",type(List_PII)) 
#
#pii_doc = FullDoc(sd_pii = 'S1674927814000082')
#if pii_doc.read(client):
#    print ("pii_doc.title: ", pii_doc.title)
#    pii_doc.write()   
#else:
#    print ("Read document failed.")
#
#
#for i in List_PII:
#    
#    pii_doc = SD_A(sd_pii =i)
#    if pii_doc.read(client):
#        print ("pii_doc.title: ", pii_doc.title)
#        #print ("\n\n","Title : \n\n ", pii_doc.title,"\n\n")
#        pii_doc.write()   
#    else:
#        print ("Read document failed.")
#
#pii_doc = FullDoc(sd_pii = 'S1674927814000082')
#if pii_doc.read(client):
#    print ("pii_doc.title: ", pii_doc.title)
#    pii_doc.write()   
#else:
