import logging

from article_scrap.ass_article import log as ass_log
from article_scrap.ass_article import ASSArticle

from nlp_filtering.ass_filtering import log as filter_log
from nlp_filtering.ass_filtering import ASSFilter

from text_mining.ass_tfidf import ASSMiner

import os
import glob

logging.basicConfig()
log = logging.getLogger("ass.mining")

log.setLevel(logging.INFO)
ass_log.setLevel(logging.WARNING)
filter_log.setLevel(logging.DEBUG)


data_folder = os.getcwd() + "/data"
files = [f for f in glob.glob(data_folder + "/*.txt")]

ass_filter = ASSFilter("Synthetic population", 5, "Multi-agent simulation", 1,
                       "micro simulation", 1, "agent initialization", 3,
                       "entity initialization", 3)

filtered_articles = ass_filter.filter([ASSArticle(open(f)) for f in files])

log.info("There is "+str(len(filtered_articles))+" article that match filter")

ass_miner = ASSMiner(filtered_articles[1::2])

tfidf_corpus: dict = ass_miner.tfidf(tfidf="sk")

# TODO : filter to have the most salient word for tf-idf
