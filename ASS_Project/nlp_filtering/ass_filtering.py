import logging
import re
import pandas

from ASS_Project.article_scrap.ass_article import ASSArticle

from ass_constant import TITLE_TAG as TITLE
from ass_constant import ABSTRACT_TAG as ABSTRACT
from ass_constant import CONTENT_TAG as CONTENT
from ass_constant import ISSN_TAG as ISSN

log = logging.getLogger("filtering")
log.setLevel(logging.INFO)

SCORE = "SCORE"
DISTANCE_COEFFICIENT = "match_distance_coefficient"

DEFAULT_SCORE_MATRIX = {TITLE: 1, ABSTRACT: 0.8, CONTENT: 0.5, DISTANCE_COEFFICIENT: 0.5}


class ASSFilter:
    _score_matrix: dict = {}
    _matches: list = []
    _matches_weight: list = []

    def __init__(self, *args, matrix=DEFAULT_SCORE_MATRIX):
        """
        In order to init filters you need a set of matches words and/or sentences
        :type args: string
        """
        log.debug("Matrix = " + str(matrix[TITLE]))
        self._score_matrix = matrix
        self._matches = args[::2]
        log.debug("Matches = " + str(self._matches))
        self._matches_weight = args[1:][::2]
        log.debug("Weights = " + str(self._matches_weight))

    def filter(self, articles, score_threshold=1, score_ratio=0.0, article_count=0):
        """
        To filter a given set of article (ASSArticle)
        :param articles: the set of articles to filter
        :param score_threshold: the score threshold
        :param score_ratio: the score ratio to filter
        :param article_count: the number of article you want to get
        :return: the filtered set of articles
        """
        if isinstance(articles, pandas.DataFrame):
            return self._df_scores(articles, score_threshold, score_ratio, article_count)
        else:
            return self._ass_scores(articles, score_threshold, score_ratio, article_count)

    def _ass_scores(self, ass_articles, score_threshold, score_ratio, article_count):
        """
        Private method to filter ASSArticle according to scores
        """
        dic: dict = {}
        for a in ass_articles:
            score = self.get_score(a)
            if score > score_threshold:
                dic[a] = score
        article_ratio = int(len(dic) * score_ratio)
        article_ratio = article_ratio if (article_count == 0 or article_count > article_ratio) else article_count
        log.debug("Expected number of filtered article " + str(article_ratio) + " over " + str(len(dic)))
        listed_article = sorted(dic.items(), key=lambda kv: (kv[1], kv[0]))
        return listed_article[-article_ratio:-1]

    def _df_scores(self, df_articles, score_threshold, score_ratio, article_count, labels=[]):
        """
        Private method to filter DataFrame according to the score of row based article
        """
        authorized_tag = [TITLE, ABSTRACT, CONTENT]
        labels = labels if all(t in labels for t in authorized_tag) else authorized_tag
        score_df = pandas.DataFrame(columns=[ISSN, CONTENT, SCORE])
        for i, row in df_articles.iterrows():
            score = sum(self.get_match_score(row[TAG], TAG) for TAG in labels if isinstance(row[TAG], str)
                        and row[TAG].strip())
            if score > score_threshold:
                new_row: dict = {ISSN: row[ISSN], CONTENT: row[CONTENT], SCORE: score}
                score_df = score_df.append(new_row, ignore_index=True)
        log.debug("Filtered DF of size "+str(len(score_df.index))+" have score "+str(score_df[SCORE])+" length")
        article_ratio = int(len(df_articles.index) * score_ratio)
        article_ratio = article_ratio if (article_count == 0 or article_count > article_ratio) else article_count
        return score_df.sort_values(SCORE, ascending=False).head(article_ratio) if len(score_df.index) > article_ratio \
            else score_df

    def get_score(self, article):
        """
        Get the score for this article
        :param self: the filter to be used
        :param article: the article to have score of
        :return: the score of the article
        """
        try:
            title = article.title()
            abstract = article.abstract()
            content = article.text()
        except RuntimeError:
            raise ValueError("Provided article is not a " + str(ASSArticle))
        return self.get_match_score(title, TITLE) * self._score_matrix[TITLE] + \
               self.get_match_score(abstract, ABSTRACT) * self._score_matrix[ABSTRACT] + \
               self.get_match_score(content, CONTENT) * self._score_matrix[CONTENT]

    def get_match_score(self, text, section=TITLE):
        """
        Get relative score according to weights (_score_matrix) and textual distance
        :param section: the section of article to scored
        :param text: the text to look match in
        :return: the relative match score
        """
        if not any(section == s for s in {TITLE, ABSTRACT, CONTENT}):
            raise ValueError("section argument must match one article entry: " + {TITLE, ABSTRACT, CONTENT})
        s = 0
        for m in self._matches:
            ms = m.split()
            sm = 0
            if len(ms) > 1:
                i = 0
                while i < len(ms) - 1:
                    dist = self.distance(text, ms[i], ms[i + 1])
                    if dist > 0:
                        sm += 1 / (dist ** self._score_matrix[DISTANCE_COEFFICIENT])
                    i += 1
            else:
                sm = 1 if re.search(m, text, re.IGNORECASE) else 0
            s += sm * self._matches_weight[self._matches.index(m)]
        return s * self._score_matrix[section]

    @staticmethod
    def distance(s, w1, w2):
        """
        Taken from https://www.geeksforgeeks.org/minimum-distance-between-words-of-a-string/
        :param s:
        :param w1:
        :param w2:
        :return:
        """
        if w1 == w2:
            return 0

            # get individual words in a list
        words = s.split(" ")
        n = len(words)

        # assume total length of the string as
        # minimum distance
        min_dist = n + 1

        # Find the first occurrence of any of the two
        # numbers (w1 or w2) and store the index of
        # this occurrence in prev
        for i in range(n):

            if ASSFilter.safe_match(words[i], w1) or ASSFilter.safe_match(words[i], w2):
                prev = i
                break

        # Traverse after the first occurrence
        while i < n:
            if ASSFilter.safe_match(words[i], w1) or ASSFilter.safe_match(words[i], w2):

                # If the current element matches with
                # any of the two then check if current
                # element and prev element are different
                # Also check if this value is smaller than
                # minimum distance so far
                if not ASSFilter.safe_match(words[prev], words[i]) and (i - prev) < min_dist:
                    min_dist = i - prev
                    prev = i
                else:
                    prev = i
            i += 1

        return min_dist

    @staticmethod
    def safe_match(w1, w2):
        try:
            return re.match(w1, w2, re.IGNORECASE)
        except re.error:
            return w1 == w2
