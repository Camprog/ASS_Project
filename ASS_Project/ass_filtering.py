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

ass_filter = ASSFilter("Synthetic population", 5, "Multi-agent simulation", 1,
                       "micro simulation", 1, "agent initialization", 3)

filtered_articles = ass_filter.filter([ASSArticle(open(f)) for f in files])

print("There is "+str(len(filtered_articles))+" article that match filter")

i = 1
for a in [x[0] for x in filtered_articles]:
    print(a.title(), ass_filter.get_score(a))
    res_file = data_folder+"/filtered/fa_"+str(i)+".txt"
    os.makedirs(os.path.dirname(res_file), exist_ok=True)
    a.save(res_file)
    i += 1
