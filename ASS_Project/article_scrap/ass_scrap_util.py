import random
from urllib import request

import bs4
import re
import logging

slash_conversion = "_Alt47_"

base_url = "http://jasss.soc.surrey.ac.uk/"
index_url = "http://jasss.soc.surrey.ac.uk/index_by_issue.html"
separator = '/'

jasss_biblio_match = "References"

jasss_meta_tag = "meta"
jasss_meta_name = "name"
jasss_meta_content = "content"

art = {"title": "arttitle", "doi": "artdoi"}

meta = {"title": "DC.Title",
        "authors": "DC.Creator",
        "abstract": ("DC.Description", "DC.Abstract"),
        "date": "DC.Date",
        "tags": "DC.Subject",
        "doi": "DC.Identifier.DOI"}

log = logging.getLogger("ass.util")


def get_latest_url():
    """Get the latest possible article from JASSS
    :return: the url reference to the page of the last to date JASSS article
    """
    req = request.urlopen(index_url).read()
    index_page = bs4.BeautifulSoup(req, "lxml")
    return index_page.find("p", {'class': 'item'}).find("a")['href']


def get_any_url():
    """Get a random url from first to last JASSS article
    :return: the url reference of any article from JASSS
    """
    req = request.urlopen(index_url).read()
    index_page = bs4.BeautifulSoup(req, "lxml")
    list_of_url = index_page.find_all("p", {'class': 'item'})
    return random.choice(list_of_url).find("a")['href']


def doi_converter(article_doi):
    """
    
    :param article_doi: the DOI as a string
    :return: the_doi converted from or to encoding version
    """
    if article_doi == "NA" or re.match("[0-9]-[0-9]-[0-9]", article_doi):
        return article_doi
    elif "/" in article_doi:
        return article_doi.replace("/", slash_conversion)
    elif slash_conversion in article_doi:
        return article_doi.replace(slash_conversion, "/")


def clean_text(text, regex_replace_dict: dict):
    """
    Clean the text using a dictionary of key=Regex value=Replacement
    :param text: the text to be clean
    :param regex_replace_dict: a dictionary of Regex: replacement
    :return: A clean version of the content of the article
    """
    
    for rx, rp in regex_replace_dict.items():
        text = rx.sub(rp if rp else '', text)
    return clean_text
    
    
def text_cleaner(text):
    """remove undesired characters in a text"""
    log.info("Regex:text_cleaner ")
    text = str(text)
    clean_txt = ''.join(character for character in text if ord(character) < 128)
    clean_txt = re.sub(r'(Introduction.*?Introduction.*?(\W))',' ', clean_txt)
    #clean_txt = re.sub(r'(Introduction.*?Introduction.*?(\W))',' ', clean_txt)
    
    # clean_text(clean_txt, {
    #     re.compile(r'(\n|\t)'): ' ',
    #     re.compile(r'https\S+'): '',
    #     re.compile(r'http\S+'): '',
    #     re.compile(r'\S+\.(gif|png|jpg|jpeg|sml|pdf|docx|doc)'): '',
    #     re.compile(r'(APPLICATION|IMAGE-DOWNSAMPLED|IMAGE-HIGH-RES|ALTIMG|IMAGE-THUMBNAIL|PDF|IMAGE-WEB-)'): '',
    #     re.compile(r'[^a-zA-Z0-9_, ]'): '',
    #     re.compile(r'((gr+\d+\W+\d+)|(Fig+\W+\d)|\d+ Elsevier |\d*jecolmodel|\w\d+|[A-Z]+[A-Z]| \d )'): ''
    # })
    clean_txt = re.sub(r'(\n|\t)',' ', clean_txt)
    clean_txt = re.sub(r'https\S+',' ', clean_txt)
    clean_txt = re.sub(r'http\S+',' ', clean_txt)
    clean_txt = re.sub(r'\S+\.(gif|png|jpg|jpeg|sml|pdf|docx|doc)',' ', clean_txt)
    clean_txt = re.sub(r'(APPLICATION|IMAGE-DOWNSAMPLED|IMAGE-HIGH-RES|ALTIMG|IMAGE-THUMBNAIL|PDF|IMAGE-WEB-)',' ',clean_txt)
    clean_txt = re.sub(r'[^a-zA-Z0-9_, ]',' ', clean_txt)
    
    #clean_txt = re.sub(r'.*(1. Introduction(?!.*1. Introduction))',' ', clean_txt)
    clean_txt = re.sub(r'(References(?!.*References)).*',' ', clean_txt)
    clean_txt = re.sub(r'(Appendix A(?!.*Appendix A)).*',' ', clean_txt)
    
    clean_txt = re.sub(r'((gr+\d+\W+\d+)|(Fig+\W+\d)|\d+ Elsevier |\d*jecolmodel|\w\d+|[A-Z]+[A-Z]| \d )',' ',
                        clean_txt)
    clean_txt = re.sub(r'  ',' ', clean_txt)
    clean_txt = re.sub(r'  ',' ', clean_txt)
    clean_txt = re.sub(r'  ',' ', clean_txt)
    clean_txt = re.sub(r'  ',' ', clean_txt)
    clean_txt = re.sub(r'.*(All rights reserved)','', clean_txt)
    clean_txt = re.sub(r'(Acknowledgements(?!.*Acknowledgements)).*',' ', clean_txt)
    
#    clean_txt = re.compile(r'(\n|\t)').sub('', clean_txt)
#    clean_txt = re.compile(r'https\S+').sub('', clean_txt)
#    clean_txt = re.compile(r'http\S+').sub('', clean_txt)
#    clean_txt = re.compile(r'\S+\.(gif|png|jpg|jpeg|sml|pdf|docx|doc)').sub('', clean_txt)
#    clean_txt = re.compile(r'(APPLICATION|IMAGE-DOWNSAMPLED|IMAGE-HIGH-RES|ALTIMG|IMAGE-THUMBNAIL|PDF|IMAGE-WEB-)')\
#        .sub('', clean_txt)
#    clean_txt = re.compile(r'[^a-zA-Z0-9_, ]').sub('', clean_txt)
#    clean_txt = re.compile(r'((gr+\d+\W+\d+)|(Fig+\W+\d)|\d+ Elsevier |\d*jecolmodel|\w\d+|[A-Z]+[A-Z]| \d )')\
#        .sub('', clean_txt)

    return clean_txt


def text_clean(text, firstauthor):
    
    txt_1 = "[\s\S]*{}".format(firstauthor)
    text_1 = re.sub(r'%s'%txt_1,"",text)
    text_sub = re.sub(r'(1\.1|2)\W.*', '', text_1)
    log.debug("\n\n\n\n\n2eme étape :", text_sub)
    
    text_alone = re.sub(r'[\S+\s]*%s'%text_sub, "", text_1)
    text_alone = re.sub(r'[^a-zA-Z0-9_,]', "", text_alone)
    
    return text_alone


#def concat_title(title):
#    
#    title = str(title)
#    title_concat = re.sub("  ","",title)
#    
#    return title_concat
    

#def remove_word(text):
#    x = [r'DOWNSAMPLED',r'IMAGE-HIGH-RES']
#    for i in x:
#        clean_txt = re.sub(i,'',text)
#        return clean_txt