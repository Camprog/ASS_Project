import logging
import re

from ASS_Project.article_scrap.ass_article import ASSArticle

log = logging.getLogger("filtering")
log.setLevel(logging.INFO)

TITLE = "title"
ABSTRACT = "abstract"
CONTENT = "content"
DISTANCE_COEFFICIENT = "match_distance_coefficient"

DEFAULT_SCORE_MATRIX = {TITLE: 1, ABSTRACT: 0.8, CONTENT: 0.5, DISTANCE_COEFFICIENT: 1 / 2}


class ASSFilter:
    _score_matrix: dict = {}
    _matches: list = []

    def __init__(self, matrix=DEFAULT_SCORE_MATRIX, *args):
        """
        In order to init filters you need a set of matches words and/or sentences
        :type args: string
        """
        self._score_matrix = matrix
        self._matches = args

    def filter(self, score_threshold=1, score_ratio=0.0, article_count=0, *args):
        """
        To filter a given set of article (ASSArticle)
        :param self:
        :param score_threshold: the score threshold
        :param score_ratio: the score ratio to filter
        :param article_count: the number of article you want to get
        :param args: the set of articles to filter
        :return: the filtered set of articles
        """
        dic: dict = {}
        for a in args:
            score = self.get_score(a)
            if score > score_threshold:
                dic[a] = score
        article_ratio = len(dic) * score_ratio
        listed_article = sorted(dic.items(), key=lambda kv: (kv[1], kv[0]))
        return listed_article[-(article_count if article_count < article_ratio else article_ratio):-1]

    def get_score(self, article):
        """
        Get the score for this article
        :param self: the filter to be used
        :param article: the article to have score of
        :return: the score of the article
        """
        if article is not ASSArticle:
            raise ValueError("article argument must be of " + ASSArticle + " type")
        t_score = self.get_match_score(ASSArticle(article).title(), TITLE)
        a_score = self.get_match_score(ASSArticle(article).abstract(), ABSTRACT)
        c_score = self.get_match_score(ASSArticle(article).text(), CONTENT)
        return t_score * self._score_matrix[TITLE] + \
               a_score * self._score_matrix[ABSTRACT] + \
               c_score * self._score_matrix[CONTENT]

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
            if len(ms) > 1:
                i = 0
                while i < ms - 1:
                    s += 1 / (self.distance(text, ms[i], ms[i + 1]) ** self._score_matrix[DISTANCE_COEFFICIENT])
            else:
                s += 1 if re.search(m, text) else 0
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

            if words[i] == w1 or words[i] == w2:
                prev = i
                break

        # Traverse after the first occurrence
        while i < n:
            if words[i] == w1 or words[i] == w2:

                # If the current element matches with
                # any of the two then check if current
                # element and prev element are different
                # Also check if this value is smaller than
                # minimum distance so far
                if words[prev] != words[i] and (i - prev) < min_dist:
                    min_dist = i - prev
                    prev = i
                else:
                    prev = i
            i += 1

        return min_dist
