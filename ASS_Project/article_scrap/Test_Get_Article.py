#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:44:26 2019

@author: camillelamy
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 15:59:34 2019

@author: camillelamy
"""

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
from ASS_Project.article_scrap.ass_article import ScienceDirectArticle as SD_A
import os


    
## Load configuration
con_file = open(os.getcwd()+"/ASS_Project/article_scrap/config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])


## ScienceDirect (full-text) document example using PII

with open(os.getcwd()+"/ASS_Project/article_scrap/list_pii_RTM.json") as json_file:  
    pii_code = json.load(json_file)
#print ("Liste des codes PII :",pii_code)
#print (type(pii_code))




List_PII = re.sub("[^\w]", " ",  pii_code).split()
#print ("List_PII",List_PII)
#print ("List_PII type",type(List_PII)) 

#
#for i in List_PII:
#    
#    pii_doc = FullDoc(sd_pii = i)
#    print (pii_doc.read(client))
#    print(pii_doc.title)
#    if pii_doc.read(client):
#        pii_doc.write()   
#    else:
#        print ("Read document failed.")
#    
#    Abstract = pii_doc.data["coredata"]["dc:description"]
#    print (Abstract)
   
for i in List_PII:
    
    ass_doc = SD_A(i, client)
    
    print (ass_doc.abstract())
    print ("pii_doc.title: ", ass_doc.title())
    ass_doc._sd_article.write()   
    
    
    """
    

    
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



print ("Revue: \n\n ",Revue,"\n\n")
print ("Keywords: \n\n ",Keywords,"\n\n")
print ("Author:\n\n",Author,"\n\n")
"""
#itérer pour Keyword et Author
"""

"""
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
