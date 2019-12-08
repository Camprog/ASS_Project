from article_scrap.ass_article import log as ass_log
from article_scrap.ass_article import ASSArticle

from nlp_filtering.ass_filtering import log as filter_log
from nlp_filtering.ass_filtering import ASSFilter


from text_mining.ass_miner import ASSMiner
from text_mining.ass_miner import log as miner_log
import logging

from random import sample

import os
import glob

import operator

import re

logging.basicConfig()
log = logging.getLogger("ass.mining")

log.setLevel(logging.INFO)
ass_log.setLevel(logging.WARNING)
filter_log.setLevel(logging.INFO)
miner_log.setLevel(logging.INFO)

#%% Main cell

data_folder = os.getcwd() + "/data"
files = [f for f in glob.glob(data_folder + "/*.txt")]

nb_article = 10
best_tfidf = 20
fltr: bool = False

if fltr:
    ass_filter = ASSFilter("Synthetic population", 5, "Multi-agent simulation", 1, "micro simulation", 1,
                           "agent initialization", 3, "entity initialization", 3)
    filtered_articles = ass_filter.filter([ASSArticle(open(f)) for f in files], article_count=nb_article)
    ass_miner = ASSMiner(filtered_articles[1::2])
    log.info("There is " + str(len(filtered_articles)) + " article that match filter")
else:
    filtered_articles = [ASSArticle(open(f)) for f in glob.glob(os.getcwd() + "/data/filtered/*.txt")]
    ass_miner = ASSMiner(sample(filtered_articles, nb_article))

tfidf_corpus: dict = ass_miner.tfidf()

mw: dict = {}
min_tfidf = 0
for a in tfidf_corpus:
    log.info("Trying to keep 100 highest TF-IDF for article " + a.title())
    sorted_tfidf = dict(sorted(tfidf_corpus[a].items(), key=operator.itemgetter(1), reverse=True))
    log.info("=> " + str(list(sorted_tfidf.items())[:best_tfidf]))
    if mw:
        sorted_tfidf = dict(filter(lambda kv: kv[1] > min_tfidf, sorted_tfidf.items()))
        log.info("filter tf-idf higher than " + str(min_tfidf))
        sorted_new_tfidf: dict = {}
        for ww in set(mw.keys()).intersection(set(sorted_tfidf.keys())):
            sorted_new_tfidf[ww] = sorted_tfidf[ww] if ww not in mw or sorted_tfidf[ww] > mw[ww] else mw[ww]
        for ww in set(mw.keys()).symmetric_difference(set(sorted_tfidf.keys())):
            sorted_new_tfidf[ww] = sorted_tfidf[ww] if ww in sorted_tfidf.keys() else mw[ww]
        mw = dict(sorted(sorted_new_tfidf.items(), key=operator.itemgetter(1), reverse=True))
    else:
        mw = sorted_tfidf
    mw_tmp = list(mw.items())[:best_tfidf]
    log.info("Temporary MW > "+str(mw))
    log.info("Sorted and cut MW "+str(mw_tmp))
    # log.info("Min TF-IDF is : "+str(mw_tmp[-1]))
    min_tfidf = mw_tmp[-1][1]
    mw = dict(mw_tmp)

log.info("Here is the result of the "+str(len(mw))+" best tfidf: ")
log.info(mw)

log.info("Now move to LDA: ")
lda = ass_miner.ass_lda(5)
log.info(ASSMiner.display_topics(lda, ass_miner.ass_feat_name, 4))
