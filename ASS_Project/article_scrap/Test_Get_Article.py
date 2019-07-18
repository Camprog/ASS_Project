#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:44:26 2019

@author: camillelamy
"""

from elsapy.elsclient import ElsClient
from JasssArticle import ScienceDirectArticle as SD_A
import json
import re

## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])


with open("list_pii_RTM.json") as json_file:  
    pii_code = json.load(json_file)
print ("Liste des codes PII :",pii_code)
print (type(pii_code))


List_PII = re.sub("[^\w]", " ",  pii_code).split()
print ("List_PII",List_PII)
print ("List_PII type",type(List_PII)) 


for i in List_PII:
    
    pii_doc = SD_A( sd_pii = i)
    if pii_doc.read(client):
        #print ("\n\n","Title : \n\n ", pii_doc.title,"\n\n")
        pii_doc.write()   
    else:
        print ("Read document failed.")

"""
pii_doc = FullDoc(sd_pii = 'S1674927814000082')
if pii_doc.read(client):
    print ("pii_doc.title: ", pii_doc.title)
    pii_doc.write()   
else:
    print ("Read document failed.")

"""