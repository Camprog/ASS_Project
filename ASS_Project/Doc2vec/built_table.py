#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 15:02:46 2019

@author: camillelamy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:08:32 2019

@author: camillelamy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:33:17 2019

@author: camillelamy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 18:45:02 2019

@author: camillelamy


"""
import os
import re
import yaml
import json
import pandas as pd
import csv
import nltk
import nltk
import io 
import nltk.corpus
from itertools import zip_longest
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import json
import csv
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 



list_df = []


#tbl = pd.DataFrame({"DOI" : [],
#                        "ISSN": [], 
#                        "TITLE": [],
#                        "ABSTRACT":[],
#                        "KEYWORDS": [],
#                        "CONTENT":[],
#                        "V1":[],
#                        "V2":[],
#                        "V3":[],
#                        "V4":[]
#                        })
#
#    




for i in range (1,10):
    with open(os.getcwd()+"/Test_NLP/articles_6500_copie/article_%s.txt"%i, "r") as article:
        data = article.read()  
         
    
    data_dict = yaml.load(data, Loader=yaml.FullLoader)
    
    try :
        content_raw = data_dict.get("CONTENT")
        content_raw = re.sub(r","," ",content_raw)
        
    except :
        content_raw = "none"
        
    try : 
        title_raw = data_dict.get("TITLE")
        title_raw = re.sub(r","," ",title_raw)
    except :
        title_raw = "none"
        
    try : 
        kw_raw = data_dict.get("KEYWORDS")
        kw_raw = re.sub(r","," ",kw_raw)
    except :
        kw_raw = "none"
        
    try : 
        DOI_raw = data_dict.get("DOI")
        DOI_raw = re.sub(r","," ",DOI_raw)
        
    except:
        DOI_raw = "none"
        
    try : 
        ISSN_raw = data_dict.get("ISSN")
        ISSN_raw = re.sub(r","," ",ISSN_raw)
    except:
        ISSN_raw = "none"
        
    try:
        abstract_raw = data_dict.get("ABSTRACT")
        abstract_raw = re.sub(r","," ",abstract_raw)
    except :
        abstract_raw = "none"     

    df = pd.DataFrame({"DOI" : [DOI_raw],
                            "ISSN": [ISSN_raw], 
                            "TITLE": [title_raw],
                            "ABSTRACT":[abstract_raw],
                            "KEYWORDS": [kw_raw],
                            "CONTENT":[content_raw],
                            "V1":[i],
                            "V2":[i],
                            "V3":[i],
                            "V4":[i]
                            })
    df
#    list_df.append(df)
#    print(list_df)
#    pd.concat([df[0],tbl[], ignore_index=True)
    
    #data.insert(i, )


print (df)
df.to_csv(r'Test_NLP/dataframe.csv')


"""   
with open(os.getcwd()+"/Test_NLP/dataframe.csv", 'w', encoding="UTF8", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow("v")
      wr.writerows(df)
"""