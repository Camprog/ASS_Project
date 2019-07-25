#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 09:57:57 2019

@author: ben & Cam
"""
import re
import bs4
from urllib.request import Request, urlopen
import json


#%%

def connection(url,limit):
    
    webpage = ""

    try :
        req = Request(url=url_Eco, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
    except:
        if limit > 10:
            raise Exception('NO CONNECTION')
        print("1 exc ept !")
        webpage = connection(url,limit + 1)

    return webpage


#%%
    
# volume is the volume's number - 1
volume = int

# Issue is the issue number of the volume (there is beetween 1 to 5 issue by volume)
issue = int

#Url_Eco is the url in which the PII identifying the items will be retrieved
url_Eco = ""

# list_pii is the list wich contain each PII of the required volumes and Issue
list_pii = []

#Loop that modifies in the url the volume numbers (vol) and the issue numbers (iss), in range (first desired volume, last desired volume, step)
for volume in range(125,408,1) :
    for issue in range (1,3,1):
        #URL of Ec. Mod. where iterate volume and issue by volume 
        url_Eco = "https://www.sciencedirect.com/journal/ecological-modelling/vol/{vol}/issue/{iss}".format(**{
                                                                                                            'vol':volume,
                                                                                                            'iss':issue})
        print (url_Eco)
        webpage = connection(url_Eco,0)
        page = bs4.BeautifulSoup(webpage, "lxml")
        
        all_dls = page.findAll("dl", {'class' : 'js-article'}) 
        for an_article in all_dls:
            all_as = an_article.findAll("a")
            if(len(all_as) == 2) :
                title = all_as[0].getText()
                url_page = "https://www.sciencedirect.com/" + all_as[0]["href"]
                
                #pii_ID_b is part of the URL contains PII
                pii_ID_b = all_as[0]["href"]
                
                #pii_ID_b filtered for extract only PII
                pii_ID = [re.sub("/science/article/pii/","",pii_ID_b)]
                
                #iteration for add PII in the PII list
                list_pii = list_pii + pii_ID
                
                #list set of list for remove duplicates
                list_pii = list(set(list_pii))
                #print(len(list_pii))
                
    print (volume, len(list_pii))
    
print("There is ",len(list_pii),",ID pii in the liste of d'écological modeling articles  : \n",list_pii)


jsonlist_pii_EM = json.dumps(list_pii)
with open('list_pii_EM.json','w') as outfile:  
    json.dump(jsonlist_pii_EM,outfile)


# the result is a JSON string:
print("Liste JSON :",jsonlist_pii_EM)
print (type(jsonlist_pii_EM)) 

print("Liste JSON :",jsonlist_pii_EM)

    
        
""" list_pii_2 = []
    for i,x in enumerate(list_pii):
        if x[0] == 'S':
            list_pii_2.append(x)"""
            
            


#virer index, trouver solution issue (2009_ 220 => 2011- 222/223), vieux pdf
#trouver une solution pout que les itération s'arrete lorsque qu'il n'y a plus d'Issue. 
