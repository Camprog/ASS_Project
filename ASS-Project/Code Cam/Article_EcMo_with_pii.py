#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 09:57:57 2019

@author: Cam
"""

from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
import json
    
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])


## ScienceDirect (full-text) document example using PII
pii_doc = FullDoc(sd_pii = 'S030438000600367X')

if pii_doc.read(client):
    print ("\n\n","Title : \n\n ", pii_doc.title,"\n\n")
    pii_doc.write()   
else:
    print ("Read document failed.")




## Abstract, keyword, Revue, Author and texte variable, go to searsh information in data folder. 
    
    
    
Abstract = pii_doc.data["coredata"]["dc:description"]
Keywords = (pii_doc.data["coredata"]["dcterms:subject"][0]["$"],
            pii_doc.data["coredata"]["dcterms:subject"][1]["$"],
            pii_doc.data["coredata"]["dcterms:subject"][2]["$"],)
Revue = pii_doc.data["coredata"]["prism:publicationName"]
"""Author = (pii_doc.data["coredata"]["dc:creator"][0]["$"],
          pii_doc.data["coredata"]["dc:creator"][1]["$"],
          pii_doc.data["coredata"]["dc:creator"][2]["$"],)"""
          
Text = pii_doc.data["originalText"]


print ("Revue: \n\n ",Revue,"\n\n")
print ("Abstract: \n\n ",Abstract,"\n\n")
print ("Keywords: \n\n ",Keywords,"\n\n")
#print ("Author:\n\n",Author,"\n\n")