# ASS-Project
Scrap and classy scientifics articles. 


Prerequisites

    An API key from http://dev.elsevier.com
    Python 3.x on your machine, with the Requests HTTP library added. If you have neither installed yet, you might want to get the Anaconda distribution of Python 3.6 go get both in one go (plus a lot of other useful stuff)
    A network connection at an institution that subscribes to Scopus and/or ScienceDirect
    Some knowledge of Python and object-oriented design
    
Quick start

    Run pip install elsapy from your command line
    In your project root folder, create a config file and add your APIkey to it
    Open Cam Code to extract information from Ecologicol modeling and RTM_prtB

Cam Code :

First : config.json ==> ad your API Key in this json.
Then, execute the code as shown below. The JSON file containing the information of the item requested in the "Article_EcMo_with_pii.py" code will be added to the data folder.



For Ecological modeling:

 	PII_Eco_Mod.py: Extract the PII identifiers from the articles, modify the volume numbers in the "in range" to be analyzed as indicated in the code.

	Article_EcMo_with_pii.py: Enter your PII like this pii_doc = FullDoc(sd_pii = 'Your PII')
  
  
  *************************
  
For Research transport part B:
  
  Same that EcMo.
  
	PII_RTM_PART_B.py 
	Article_RTM_PART_B_with_pii.py 	
  
	 	
  
		
  
	
