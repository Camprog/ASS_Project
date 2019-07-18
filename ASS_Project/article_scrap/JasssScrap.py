import random
from urllib import request

import bs4
import re

from itertools import product

from .JasssArticle import JasssArticle

slash_conversion = "_Alt47_"

base_url = "http://jasss.soc.surrey.ac.uk/"
index_url = "http://jasss.soc.surrey.ac.uk/index_by_issue.html"
separator = '/'

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


def visit_article(volume=1, number=1, article=1):
    """Retrieve article from JASSS based on the value of volume, number and article

    :param int volume:
    :param int number:
    :param int article:
    :return: an html page that represents requested article
    """
    return JasssArticle(volume, number, article)


def visit_articles(to_volume=(1, 1), to_number=(1, 4), to_article=(1, 1)):
    """Retrieve a collection of articles from 1 to args volume, issue and article found in JASSS

    :param int to_volume: the max number of volume; between 1 and ongoing number of volume
    :param int to_number: the max number of issue; between 1 and 4
    :param int to_article: the max number of article; between 1 and the number of article for current volume and issue
    :return: a tuple made of html pages
    """
    return [visit_article(x, y, z) for x, y, z in
            product(max(1, range(to_volume[0]), to_volume[1]),
                    range(max(1, to_number[0]), min(4, to_number[1])),
                    range(max(1, to_article[0])), to_article[1])]


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


def clean_text(text):
    """

    :return: A clean version of the content of the article
    """
    intro_split = re.split('\nintroduction\n', text, re.IGNORECASE)
    print(intro_split)
