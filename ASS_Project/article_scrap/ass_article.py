import json
from abc import abstractmethod

import requests

from bs4 import BeautifulSoup
from elsapy.elsdoc import FullDoc
from requests import HTTPError

from ASS_Project.article_scrap import jasss_scrap_util


class ASSArticle:

    title_tag = "TITLE"
    abstract_tag = "ABSTRACT"
    keywords_tag = "KEYWORDS"
    text_tag = "CONTENT"

    def __init__(self, file):
        json_content = json.load(file)
        self._title = json_content[self.title_tag]
        self._abstract = json_content[self.abstract_tag]
        self._keywords = json_content[self.keywords_tag]
        self._content = json_content[self.text_tag]

    @abstractmethod
    def title(self):
        return self._title

    @abstractmethod
    def abstract(self):
        return self._abstract

    @abstractmethod
    def keywords(self):
        return self._keywords

    @abstractmethod
    def text(self):
        return self._content

    def save(self, res_file):
        file = open(res_file, "w")

        file.write(json.dumps(
            {
                self.title_tag: self.title(),
                self.abstract_tag: self.abstract(),
                self.keywords_tag: self.keywords(),
                self.text_tag:  self.text()
            }
        ))

        file.close()


class JasssArticle(ASSArticle):
    bs_article: BeautifulSoup

    def __init__(self, *args, **kwargs):
        # args -- tuple of anonymous arguments
        # kwargs -- dictionary of named arguments
        """init article from an url
        *args
        :param int volume:
        :param int issue:
        :param int article:
        **kwargs
        :param url url:
        """
        if len(args) == 0:
            req = requests.get(kwargs.get('url', jasss_scrap_util.get_latest_url()))
            if req.status_code == requests.codes.ok:
                self.url = req.url
                self.bs_article = BeautifulSoup(req.content, 'html5lib')
            else:
                raise HTTPError(req.reason)
        else:
            basic_url = jasss_scrap_util.base_url + str(args[0]) + jasss_scrap_util.separator + str(args[1]) + jasss_scrap_util.separator
            req = requests.get(basic_url + str(args[2]) + jasss_scrap_util.html)
            self.url = req.url
            if req.status_code == requests.codes.ok:
                self.bs_article = BeautifulSoup(req.content, 'html5lib')
            else:
                self.bs_article = BeautifulSoup(requests.get(basic_url + str("review" + args[2]) + jasss_scrap_util.html),
                                                'html5lib')

    def __repr__(self):
        return self.url

    def is_review(self):
        """ Tells if this article is a review or not """
        return True if "review" in self.__repr__() else False

    def keywords(self):
        """
        Get the key worlds from an article
        :param html bs_article:
        :return: a tuple made of key worlds
        """
        return [x.strip() for x in self.get_meta_content_with_tag("tags").split(',')]

    def title(self):
        """ Retrieve the title of the article """
        return self.get_meta_content_with_tag()

    def authors(self):
        """
        Retrieve the authors of the article
        :param html bs_article:
        :return: a tuple of authors
        """
        return [x.strip() for x in self.get_meta_content_with_tag("authors").split(';')]

    def abstract(self):
        """ Retrieve the abstract of the article"""
        the_abstract = self.get_meta_content_with_tag("abstract")

        if len(the_abstract.split()) < 5:
            return str(self.bs_article.find(string="Abstract").findNext("dl").next.contents[0]).strip()
        return the_abstract

    def doi(self):
        """
        Give the DOI stored in meta data
        :return: a unique *string* that represent this article
        """
        if self.is_review():
            return self.__repr__()
        try:
            doi = self.get_meta_content_with_tag("doi")
        except TypeError:
            doi = self.get_art_content_with_tag("doi")
        return doi

    def text(self):
        """
        :return: The plain text of the article
        """
        body = self.bs_article.findAll("article")
        if len(body) == 1:
            return body[0].getText()
        else:
            art = self.bs_article.findAll("div", {'class': 'article'})
            if len(art) > 0:
                return art[0].getText()
            else:
                if len(art) == 0:
                    art = self.bs_article
                body = art.find("body")
                the_ps = body.findAll("p")
                for ppps in the_ps:
                    ppps.extract()
                dls = body.findAll("dl")
                if len(dls) > 0:
                    dds = dls[0].findAll("dd")
                    if len(dds) > 1:
                        dds[0].extract()
                        dds[1].extract()

                return body.getText()

    def get_meta_content_with_tag(self, tag="title"):
        """
        Retrieve the content of a tag as define by *beautifulsoup*
        :param string tag: the tag to find in the soup
        :return: a string representation of the content of the tag
        """
        m_name = jasss_scrap_util.jasss_meta_name
        m_content = jasss_scrap_util.jasss_meta_content
        if self.bs_article.find_next(jasss_scrap_util.jasss_meta_tag,
                                     {jasss_scrap_util.jasss_meta_name.upper(): "title"}):
            m_name = jasss_scrap_util.jasss_meta_name.upper()
            m_content = jasss_scrap_util.jasss_meta_content.upper()

        if isinstance(jasss_scrap_util.meta[tag], str):
            meta_context = self.bs_article.find(jasss_scrap_util.jasss_meta_tag,
                                                {m_name: jasss_scrap_util.meta[tag]})
        else:
            for tg in jasss_scrap_util.meta[tag]:
                meta_context = self.bs_article.find(jasss_scrap_util.jasss_meta_tag, {m_name: tg})
                if meta_context is not None:
                    break
        return meta_context[m_content]

    def get_art_content_with_tag(self, tag="title"):
        """
        Retrieve the content of a tag define in the *art* section of JASSS article pages
        :param tag:
        :return: a string representation of the content of the tag
        """
        balise: str = "p"
        if tag == "doi":
            balise = "span"
        result = self.bs_article.find(balise, {'class': jasss_scrap_util.art[tag]})
        if result is None:
            return "-".join([str(s) for s in self.__repr__() if s.isdigit()])
        if tag == "doi":
            result = result.contents[0].replace('DOI:', '')
        return result.strip()

    def get_soup(self):
        """
        
        :return: the soup of the source retrieve by *beautifulsoup* 
        """
        return self.bs_article


class ScienceDirectArticle(ASSArticle):
    #sd_article: FullDoc

    def __init__(self, *args):
        """
        
        """
        print(args[0])
        self._sd_article = FullDoc(sd_pii=args[0])
        if not self._sd_article.read(els_client=args[1]):
            raise HTTPError
            

    def title(self):
        """Gets the document's title"""
        return self._sd_article.title

    def abstract(self):
        """Gets the document's abstract"""
        return self._sd_article.data["coredata"]["dc:description"]

    def text(self):
        """Gets the document's text"""
        return self._sd_article.data["originalText"]

    def keywords(self):
        """Gets the document's Keywords"""
        try:    
            kw=self._sd_article.data["coredata"]["dcterms:subject"]
            KW_list = [item['$'] for item in kw]
            return KW_list
        except KeyError:
            KW_list = ["No Keyword"]
            return KW_list