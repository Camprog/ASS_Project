from article_scrap.ass_article import ASSArticle

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import pandas
import re
import math
import logging

SKTFIDF = "sk"
ASSTFIDF = "ass"

log = logging.getLogger("miner")
log.setLevel(logging.DEBUG)


class ASSMiner:
    """
    ASSMiner is the main ASS object to text mine a corpus of articles

    Attributes
    ----------
    articles : list
        the list of articles to mine
    asstfidf : str
        the algorithm for tfidf
    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    _articles: list = []
    _asstfidf: str
    _asslang: str
    _assfeat: int

    ass_feat_name: list = []

    def __init__(self, articles, tfidf="ass", language="english", feature_ratio=0.01):
        """
        constructor for ASSMiner
        :param articles: the corpus of article to mine
        :param tfidf: the algorithm of TF-IDF
        :param language: the language for stop-word dictionary based removal (also lem/stem)
        :param feature_ratio: the ratio of word of interest (best n * feature_ratio kept)
        """
        self._articles = articles
        self._asstfidf = tfidf
        self._asslang = language
        self._assfeat = int(sum(len(a.text().split()) for a in articles) * feature_ratio)

    def tfidf(self, tfidf="", label_tag=ASSArticle.title_tag):
        """
        Apply TF-IDF on the corpus of article of this ASSMiner
        :param label_tag: the tag to label tf-idf ASSArticle
        :param tfidf: the type of algorithm 'ass' or 'sk'
        :return: Depending on tfidf methods, either pandas dataframe or dictionary, and depending on clusters presence
        either a dictionary of tfidf per clusters (IDF is for the entire corpus) or just all tfidf per article
        """
        tfidf = tfidf if tfidf != "" else self._asstfidf
        corpus = [a.text() for a in self._articles]
        labels = self._articles if label_tag != ASSArticle.title_tag else [a.title() for a in self._articles]
        return ASSMiner._sk_tfidf(corpus) if re.match(tfidf, SKTFIDF, re.I) else ASSMiner._ass_tfidf(corpus, labels)

    @staticmethod
    def _sk_tfidf(texts):
        """
        Implementation of tf-idf from scikit-learn
        :param texts: the set of raw text to explore
        :return: a pandas data frame of the tf-idf scores
        """
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        dense_list = dense.tolist()
        return pandas.DataFrame(dense_list, columns=feature_names)

    @staticmethod
    def _ass_tfidf(texts, labels=[]):
        """
        Self made implementation of tf-idf with title labels (or default int iterator)
        :param articles: the set of articles to explore
        :return: a dictionary made as follow => [article : [word : tf-idf]]
        """
        ass_dict = {}  # Article :: list of words
        tfidf_dict = {}  # Article :: [word :: tf-idf]
        words = []  # All words
        labels = range(len(texts)) if not labels else labels
        # Set article words and total set of words
        for a, l in zip(texts, labels):
            ass_dict[l] = a.split()
            words = set(words).union(set(ass_dict[l]))

        log.debug("Word dictionary contains "+str(len(words))+" words for "+str(len(texts))+" articles")

        # Compute IDF for the entire corpus
        idf_dict = ASSMiner._idf(ass_dict.values(), words)

        # compute TF for each article
        for a, l in zip(texts, labels):
            tfidf_dict[l] = ASSMiner._tfidf(idf_dict, ass_dict[l])

        return tfidf_dict

    @staticmethod
    def _idf(splits, wd=[]):
        """
        Build IDF for a list of text (splited words)
        :param splits: the list of texts as a list of string
        :param wd: the whole list of words
        :return: IDF for each word in the list of text
        """
        corpus_len = len(splits)
        wd = wd if wd else list(set().union(*splits))
        log.debug("Dictionary : "+str(wd))
        idf_dict = {}
        for w in wd:
            idf_dict[w] = math.log(corpus_len / float(sum(w in text for text in splits)))
            log.debug("IDF of "+w+" is "+str(idf_dict[w]))
        return idf_dict

    @staticmethod
    def _tfidf(idf, text):
        """
        TF-IDF for a list of texts (splited words)
        :param idf: the dictionary of IDF for each word
        :param text: the list of texts
        :return: TF-IDF for each word in each text
        """
        split = text.split() if isinstance(text, str) else text
        log.debug(str(split))
        n = float(len(split))
        tfidf: dict = {}
        for item in map(lambda w: (w, split.count(w)), set(split)):
            log.debug("Add tf-idf for "+item[0]+" = "+str(item[1] / n * idf[item[0]]))
            tfidf[item[0]] = item[1] / n * idf[item[0]]
        return tfidf

    def ass_lda(self, topics, features=-1):
        """
        Latent Dietrich Allocation based on sklearn implementation
        :param topics: the number of topic to look for
        :param features: the number of word to take into account for topic modeling
        :return: the LDA model from sklearn
        """
        mf = features if features > 0 else self._assfeat
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=mf, stop_words=self._asslang)
        tf = tf_vectorizer.fit_transform([a.text() for a in self._articles])
        self.ass_feat_name = tf_vectorizer.get_feature_names()
        return LatentDirichletAllocation(n_components=topics, max_iter=5, learning_method='online', learning_offset=50.,
                                        random_state=0).fit(tf)

    @staticmethod
    def display_topics(model, feature_names, no_top_words):
        result: str = ""
        for topic_idx, topic in enumerate(model.components_):
            result += "\nTopic %d:" % topic_idx
            result += " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
        return result
