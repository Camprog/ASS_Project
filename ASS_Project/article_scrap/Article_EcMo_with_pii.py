#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 09:57:57 2019

@author: Cam
"""

from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
import json
import re
    
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])


## ScienceDirect (full-text) document example using PII
with open("list_pii_EM.json") as json_file:  
    pii_code_EM = json.load(json_file)
print ("Liste des codes PII :",pii_code_EM)
print (type(pii_code_EM))

List_PII_EM = re.sub("[^\w]", " ",  pii_code_EM).split()
print ("List_PII",List_PII_EM)
print ("List_PII type",type(List_PII_EM)) 

for i in List_PII_EM:
    pii_doc = FullDoc(sd_pii = i)
    
    if pii_doc.read(client):
        #print ("\n\n","Title : \n\n ", pii_doc.title,"\n\n")
        pii_doc.write()   
    else:
        print ("Read document failed.")
        
    Abstract = pii_doc.data["coredata"]["dc:description"]
    Revue = pii_doc.data["coredata"]["prism:publicationName"]
    Text = pii_doc.data["originalText"]
    
    #print (pii_doc.title,Abstract, Revue)
    Article = str(Revue)+str(pii_doc.title) + str(Abstract)+ str(Text)
    print (Article)
    
    with open("/Users/camillelamy/Dossier_Python/ASS-Project/Code_Cam/Article_EM/"+str(re.sub(" ","_",pii_doc.title))+".txt",'w') as outfile:  
        json.dump(Article, outfile)    

    print (Article)



## Abstract, keyword, Revue, Author and texte variable, go to searsh information in data folder. 
    
    
    
"""Abstract = pii_doc.data["coredata"]["dc:description"]
Keywords = (pii_doc.data["coredata"]["dcterms:subject"][0]["$"],
            pii_doc.data["coredata"]["dcterms:subject"][1]["$"],
            pii_doc.data["coredata"]["dcterms:subject"][2]["$"],)
Revue = pii_doc.data["coredata"]["prism:publicationName"]
Author = (pii_doc.data["coredata"]["dc:creator"][0]["$"],
          pii_doc.data["coredata"]["dc:creator"][1]["$"],
          pii_doc.data["coredata"]["dc:creator"][2]["$"],)
          
Text = pii_doc.data["originalText"]


print ("Revue: \n\n ",Revue,"\n\n")
print ("Abstract: \n\n ",Abstract,"\n\n")
print ("Keywords: \n\n ",Keywords,"\n\n")
#print ("Author:\n\n",Author,"\n\n")
"""