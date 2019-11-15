#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thursday Jul 4 15:43:00 2019

@author: kevin
"""
from urllib import request
from requests import HTTPError

import bs4
import os
import logging
from re import findall as fall

from pathlib import Path

from article_scrap.ass_article import log as ass_log
from article_scrap.ass_article import JasssArticle
from article_scrap.ass_scrap_util import doi_converter

logging.basicConfig()
log = logging.getLogger("ass.jasss_mining")
log.setLevel(logging.INFO)
ass_log.setLevel(logging.WARNING)

url_JASSS = "http://jasss.soc.surrey.ac.uk/index_by_issue.html"
req_text = request.urlopen(url=url_JASSS).read()

page = bs4.BeautifulSoup(req_text, "lxml")

itr = 0
rvw = 0
nb_max = len(page.findAll("p", {'class': 'item'}))
condition = False

tp = Path(os.getcwd() + "/data")

rtcl = [18, 3, 3]

#the_old_article = JasssArticle(rtcl[0], rtcl[1], rtcl[2])
#the_old_article.save(str(tp)+"/test_old_article.txt")

goon = False
for gen in page.findAll("p", {'class': 'item'}):
    itr += 1
    url_article = gen.find("a")['href']

    url_issue = [e for e in fall(r"[\w']+", url_article) if e.isdigit()]

    if url_issue == [str(rtcl[0]), str(rtcl[1]), str(rtcl[2])]:
         goon = False
    if goon:
         continue

    log.info(round(str(itr)/nb_max, 2) + "% => " + url_article + " | " + str(url_issue) + " review = "+rvw)
    try:
        article = JasssArticle(url=url_article)
    except HTTPError as e:
        print("Don't care about http request exceptions: ", e)

    if article.is_review():
        rvw += 1
        continue

    doi = article.doi()
    res_file = str(tp) + "/JASSS_" + doi_converter(doi) + ".txt"
    os.makedirs(os.path.dirname(res_file), exist_ok=True)

    article.save(res_file)
    if (itr % 10000000) == 0:
        inp = input("Type 'c' button to continue 'e' to exit")
        exit(0) if inp == 'e' else log.info("Carry on")
