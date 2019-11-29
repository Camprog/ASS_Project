import logging

from article_scrap.ass_article import log as ass_log
from article_scrap.ass_article import ASSArticle

from nlp_filtering.ass_filtering import log as filter_log
from nlp_filtering.ass_filtering import ASSFilter

import os
import glob
from pathlib import Path

logging.basicConfig()
log = logging.getLogger("ass.filter")

log.setLevel(logging.INFO)
ass_log.setLevel(logging.WARNING)
filter_log.setLevel(logging.DEBUG)


data_folder = os.getcwd() + "/data"
files = [f for f in glob.glob(data_folder + "/*.txt")]

ass_filter = ASSFilter("Synthetic population", "Multi-agent simulation", "micro simulation", "agent initialization")

filtered_articles = ass_filter.filter([ASSArticle(open(f)) for f in files], score_ratio=0.02)

print("There is "+str(len(filtered_articles))+" article that match filter")

for a in [x[0] for x in filtered_articles]:
    print(a.title(), ass_filter.get_score(a))
