import logging
import re

from ASS_Project.article_scrap.ass_article import ASSArticle

log = logging.getLogger("filtering")
log.setLevel(logging.INFO)

T = "title"
A = "abstract"
C = "content"

P = "perfect_match"
R = "relative_match"


class ASSFilter:
    _score_matrix = {T: 1, A: 0.8, C: 0.5, P: 1, R: 0.5}
    _matches = {}

    def __init__(self, matrix=_score_matrix, *args):
        """
        In order to init filters you need a set of matches words and/or sentences
        :type args: string
        """
        self._score_matrix = matrix
        self._matches = args

    def filter(self, score_threshold=-1, score_ratio=0.0, article_count=0, *args):
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
        # TODO : find the score_ratio actual score and filter list accordingly
        min_score = 1 + score_ratio
        dic = dict(filter(lambda x: dic[x] > min_score))
        return dic.keys()[-article_count]

    def get_score(self, article):
        """
        Get the score for this article
        :param self: the filter to be used
        :param article: the article to have score of
        :return: the score of the article
        """
        if article is not ASSArticle:
            raise ValueError("article argument must be of "+ASSArticle+" type")
        t_score = self.get_section_score(ASSArticle(article).title(), T)
        a_score = self.get_section_score(ASSArticle(article).abstract(), A)
        c_score = self.get_section_score(ASSArticle(article).text(), C)
        return {t_score, a_score, c_score}

    def get_section_score(self, text, section=T):
        """
        Get the score associated with a particular section of the article
        :param self: the filter
        :param text: the text to account matches for
        :param section: the specific section of article to look for among \{"title", "abstract", "content"\}
        :return: the score associated to a particular section of a given article
        """
        if not any(section = s for s in {T, A, C}):
            raise ValueError("section argument must match one article entry: "+{T, A, C})
        s = self.get_perfect_match(text)
        s = s if s > 0 else self.get_relative_match(text)
        return s * self._score_matrix[section]

    def get_perfect_match(self, text):
        """
        Score for a perfect match (exact same sequence of characters)
        :param self: the filter
        :param text: the text section to look matches for
        :return: the score
        """
        s = 0
        for m in self._matches:
            s += self._score_matrix[P] if re.search(m, text) else 0
        return s

    def get_relative_match(self, text):
        """
        TODO : make relative score relative to the distance (word distance) between part of a match
        :param text: the text to look match in
        :return: the relative match score
        """
        s = 0
        for m in self._matches:
            ms = m.split()
            if len(ms) > 1:
                i = 0
                while i < ms - 1:
                    s += 1 / self.distance(text, ms[i], ms[i+1])
            else:
                s += self._score_matrix[P] if re.search(m, text) else 0
        return s * self._score_matrix[R]

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
                    min_dist = i - prev - 1
                    prev = i
                else:
                    prev = i
            i += 1

        return min_dist


