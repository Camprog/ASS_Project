#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 11:47:13 2019

@author: camillelamy
"""
from elsapy.elsdoc import FullDoc
from JasssArticle import ASSArticle


class ScienceDirectArticle(ASSArticle):
    sd_article: FullDoc

    def __init__(self, *args):
        self.sd_article = FullDoc(sd_pii=args[0])

    def title(self):
        return self.sd_article.data["coredata"]["title"]

    def abstract(self):
        return self.sd_article.data["coredata"]["dc:description"]

    def text(self):
        return self.sd_article.data["originalText"]

    def keywords(self):
        
        return self.sd_article.data["coredata"]["dcterms:subject"]
        KW_list = [item['$'] for item in Keywords]