
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas
import re
import math

from article_scrap.ass_article import ASSArticle

SKTFIDF = "sk"
ASSTFIDF = "ass"


class ASSMiner:
    _articles: list = []
    _asstfidf: str

    def __init__(self, articles, tfidf="ass"):
        if any(not isinstance(a, ASSArticle) for a in articles):
            raise ValueError("all article from articles argument must be of " + ASSArticle + " type")
        _articles = articles
        _asstfidf = tfidf

    def tfidf(self, tdifd=_asstfidf):
        return ASSMiner.sk_tfidf(self._articles) if re.match(tdifd, SKTFIDF, re.I) \
            else ASSMiner.ass_tfidf(self._articles)

    @staticmethod
    def sk_tfidf(articles):
        """
        Implementation of tf-idf from scikit-learn
        :param articles: the set of article to explore
        :return: a pandas data frame of the tf-idf scores
        """
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(articles)
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        dense_list = dense.tolist()
        return pandas.DataFrame(dense_list, columns=feature_names)

    @staticmethod
    def ass_tfidf(articles):
        """
        Self made implementation of tf-idf
        :param articles: the set of articles to explore
        :return: a dictionary made as follow => [article : [word : tf-idf]]
        """
        ass_dict = []  # Article :: list of words
        tfidf_dict = []  # Article :: [word :: tf-idf]
        words = {}  # All words
        # Set article words and total set of words
        for a in articles:
            ass_dict[a] = a.text().split()
            words = set(words).union(set(ass_dict[a]))

        # Compute IDF for the entire corpus
        corpus_len = len(articles)
        idf_dict = []
        for w in words:
            idf_dict[w] = math.log(corpus_len / float(sum(w in ass_dict[v] for v in ass_dict.keys())))

        # compute TF for each article
        for a in articles:
            n = float(len(ass_dict[a]))
            awc = dict(map(lambda tw: (tw, ass_dict[a].count(tw)), set(ass_dict[a])))  # article world count (awc)
            tfidf_dict[a] = dict(map(lambda kv: (kv[0], kv[1] / n * idf_dict[kv[0]]), awc.items()))

        return tfidf_dict
