import re
from abc import abstractmethod

from bs4 import BeautifulSoup
from requests import HTTPError

import JasssScrap

from elsapy.elsdoc import FullDoc

class ASSArticle:

    ass_start_balise: str = "<|"
    ass_end_balise = "|>"

    title_tag = "TITLE"
    abstract_tag = "ABSTRACT"
    keywords = "KEYWORDS"

    def constructor(self, file):
        part = re.split(ASSArticle.ass_start_balise, file)

    @abstractmethod
    def title(self):
        pass

    @abstractmethod
    def abstract(self):
        pass

    @abstractmethod
    def keywords(self):
        pass

    @abstractmethod
    def text(self):
        pass

    def save(self, res_file):
        file = open(res_file, "w")

        file.write(ASSArticle.ass_start_balise + ASSArticle.title_tag)
        file.write(self.title())
        file.write(ASSArticle.ass_end_balise)
        file.write(ASSArticle.ass_start_balise + ASSArticle.keywords)
        file.write(self.keywords())
        file.write(ASSArticle.ass_end_balise)
        file.write(ASSArticle.ass_start_balise + ASSArticle.abstract_tag)
        file.write(self.abstract())
        file.write(ASSArticle.ass_end_balise)
        file.write(ASSArticle.ass_start_balise + ASSArticle.text_tag)
        file.write(self.text())
        file.write(ASSArticle.ass_end_balise)

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
            req = requests.get(kwargs.get('url', JasssScrap.get_latest_url()))
            if req.status_code == requests.codes.ok:
                self.url = req.url
                self.bs_article = BeautifulSoup(req.content, 'html5lib')
            else:
                raise HTTPError(req.reason)
        else:
            basic_url = JasssScrap.base_url + str(args[0]) + JasssScrap.separator + str(args[1]) + JasssScrap.separator
            req = requests.get(basic_url + str(args[2]) + JasssScrap.html)
            self.url = req.url
            if req.status_code == requests.codes.ok:
                self.bs_article = BeautifulSoup(req.content, 'html5lib')
            else:
                self.bs_article = BeautifulSoup(requests.get(basic_url + str("review" + args[2]) + JasssScrap.html),
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
        m_name = JasssScrap.jasss_meta_name
        m_content = JasssScrap.jasss_meta_content
        if self.bs_article.find_next(JasssScrap.jasss_meta_tag,
                                     {JasssScrap.jasss_meta_name.upper(): "title"}):
            m_name = JasssScrap.jasss_meta_name.upper()
            m_content = JasssScrap.jasss_meta_content.upper()

        if isinstance(JasssScrap.meta[tag], str):
            meta_context = self.bs_article.find(JasssScrap.jasss_meta_tag,
                                                {m_name: JasssScrap.meta[tag]})
        else:
            for tg in JasssScrap.meta[tag]:
                meta_context = self.bs_article.find(JasssScrap.jasss_meta_tag, {m_name: tg})
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
        result = self.bs_article.find(balise, {'class': JasssScrap.art[tag]})
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
    sd_article: FullDoc

    
    def __init__(self, *args):       
        self.sd_article = FullDoc(sd_pii=args[0])
            
    def title(self):
        """Gets the document's title"""
        return self.data["coredata"]["title"]

    def abstract(self):
        """Gets the document's abstract"""
        return self.data["coredata"]["dc:description"]

    def text(self):
        """Gets the document's text"""
        return self.data["originalText"]

    def keywords(self):
        """Gets the document's Keywords"""
        try:    
            kw=self.data["coredata"]["dcterms:subject"]
            KW_list = [item['$'] for item in kw]
            return KW_list
        except KeyError:
            KW_list = ["No Keyword"]
            return KW_list
    

""" 

"""