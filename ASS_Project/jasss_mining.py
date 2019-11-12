#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thursday Jul 4 15:43:00 2019

@author: kevin
"""
from urllib import request

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
condition = False

tp = Path(os.getcwd() + "/data/articles/")

the_old_article = JasssArticle(13, 1, 14)
the_old_article.save(str(tp)+"/test_old_article.txt")

# for gen in page.findAll("p", {'class': 'item'}):
#     itr += 1
#     url_article = gen.find("a")['href']
#
#     url_issue = [e for e in fall(r"[\w']+", url_article) if e.isdigit()]
#     log.info(url_article + " => " + str(url_issue))
#
#     log.info(str(itr) + " => " + url_article)
#     article = JasssArticle(url=url_article)
#
#     if article.is_review():
#         continue
#
#     res_file = str(tp) + "/JASSS_" + doi_converter(article.doi()) + ".txt"
#     os.makedirs(os.path.dirname(res_file), exist_ok=True)
#
#     article.save(res_file)
#     if (itr % 10000000) == 0:
#         inp = input("Type 'c' button to continue 'e' to exit")
#         exit(0) if inp == 'e' else log.info("Carry on")
