import logging

from article_scrap.ass_article import log as ass_log
from article_scrap.ass_article import ASSArticle

from nlp_filtering.ass_filtering import log as filter_log
from nlp_filtering.ass_filtering import ASSFilter
from nlp_filtering.ass_filtering import SCORE

from ass_constant import ISSN_TAG as ISSN

import os
import glob
import pandas

logging.basicConfig()
log = logging.getLogger("ass.filter")

log.setLevel(logging.INFO)
ass_log.setLevel(logging.WARNING)
filter_log.setLevel(logging.DEBUG)


data_folder = os.getcwd() + "/data"
files = [f for f in glob.glob(data_folder + "/*.txt")]

df_file = "df_filtered.csv"
file = data_folder+"/"+df_file if df_file else ""
df = pandas.read_csv(file)
print(df.head(0))
print(len(df.index))

issnlist = df[ISSN].tolist()

print("JASSS : "+str(issnlist.count("1460-7425")/float(len(issnlist))))
print("RT : "+str(issnlist.count("01912615")/float(len(issnlist))))
print("EM : "+str(issnlist.count("03043800")/float(len(issnlist))))

exit()

ass_filter = ASSFilter("Synthetic population", 5, "demographic data", 3, "simulation initialization", 2)

if file == "":
    filtered_articles = ass_filter.filter([ASSArticle(open(f)) for f in files])
    print("There is " + str(len(filtered_articles)) + " article that match filter")

    i = 1
    for a in [x[0] for x in filtered_articles]:
        print(a.title(), ass_filter.get_score(a))
        res_file = data_folder + "/filtered/fa_" + str(i) + ".txt"
        os.makedirs(os.path.dirname(res_file), exist_ok=True)
        a.save(res_file)
        i += 1
else:
    filtered_articles = ass_filter.filter(pandas.read_csv(file), score_ratio=0.05)
    filtered_articles.to_csv(data_folder + "/df_filtered.csv")
    print(filtered_articles[SCORE].to_string(index=False))
