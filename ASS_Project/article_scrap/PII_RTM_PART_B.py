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
        req = Request(url=url_RTM, headers={'User-Agent': 'Mozilla/5.0'})
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

#Url_RTM is the url in which the PII identifying the items will be retrieved.
url_RTM = ""

# list_pii is the list wich contain each PII of the required volumes and Issue
list_pii_RTM = []

#Loop that modifies in the url the volume numbers (vol) and the issue numbers (iss), in range (first desired volume, last desired volume, step)
for volume in range(100,101,1) :
    
    #URL of Ec. Mod. where iterate volume and issue by volume 
    for issue in range (1,2,1):
        
        url_RTM = "https://www.sciencedirect.com/journal/transportation-research-part-b-methodological/vol/{vol}/issue/{iss}".format(**{'vol':volume,'iss':issue})
        webpage = connection(url_RTM,0)
        page = bs4.BeautifulSoup(webpage, "lxml")
        print (url_RTM)
        all_dls = page.findAll("dl", {'class' : 'js-article'}) 
        # print(len(all_dls))
        for an_article in all_dls:
            all_as = an_article.findAll("a")
            if(len(all_as) == 2):
                title = all_as[0].getText()
                url_page = "https://www.sciencedirect.com" + all_as[0]["href"]
                
                #pii_ID_L is part of the URL contains PII
                pii_ID_L = all_as[0]["href"]
                
                #pii_ID filtered for extract only PII
                pii_ID = [re.sub("/science/article/pii/","",pii_ID_L)]
                
                
                      
                #iteration for add PII in the PII list
                list_pii_RTM = list_pii_RTM + pii_ID
                
                   
                #list set of list for remove duplicates
                list_pii_RTM = list(set(list_pii_RTM))
                
                #dict_pii_RTM = { i : list_pii_RTM[i] for i in range(0, len(list_pii_RTM) ) }
                
                #print(len(list_pii_RTM))
                

    
            
            
    #for pii_ID in list_pii_RTM :
    #    if str[0] != 'S':
    #        del pii_ID
    #print (volume, len(list_pii_RTM))
    
    
print("Il y a ",len(list_pii_RTM),"ID pii dans la liste le volume d'RTM_part_B: \n",list_pii_RTM)



# convert into JSON:
jsonlist_pii = json.dumps(list_pii_RTM)
with open('list_pii_RTM.json','w') as outfile:  
    json.dump(jsonlist_pii,outfile)


# the result is a JSON string:
print("Liste JSON :",jsonlist_pii)
print (type(jsonlist_pii)) 

print("Liste JSON :",jsonlist_pii)





#jsondict_pii = json.dumps(dict_pii_RTM)
#with open('dict_pii_RTM.json','w') as outfile:  
#    json.dump(jsondict_pii,outfile)


# the result is a JSON string:
#print("Dict JSON :",jsondict_pii)

# print list after removing given element
        
#for pii_ID in list_pii_RTM :
#  :
#    del pii_ID
   
#if str[0] != 'S': : 
        

           #list_pii_RTM_2 = []
        #for i,x in enumerate(list_pii_RTM):
         #   if x[0] == 'S':
          #      list_pii_RTM_2.append(x)     
  










        
        
                
                
               
                
                
           
        
    