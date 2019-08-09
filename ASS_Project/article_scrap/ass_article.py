import json
from abc import abstractmethod

import requests
import logging

from bs4 import BeautifulSoup
from elsapy.elsdoc import FullDoc
from requests import HTTPError


from ASS_Project.article_scrap import jasss_scrap_util
from ASS_Project.article_scrap.jasss_scrap_util import doi_converter 
from ASS_Project.article_scrap.jasss_scrap_util import remove_gif
import re
import unicodedata


class ASSArticle:

    doi_tag = "DOI"
    issn_tag = "ISSN"
    title_tag = "TITLE"
    abstract_tag = "ABSTRACT"
    keywords_tag = "KEYWORDS"
    text_tag = "CONTENT"

    def __init__(self, file):
        logging.debug("init ASS")
        json_content = json.load(file)
        self._title = json_content[self.title_tag]
        self._abstract = json_content[self.abstract_tag]
        self._keywords = json_content[self.keywords_tag]
        self._content = json_content[self.text_tag]
        logging.debug("init ASS end")

    @abstractmethod
    def doi(self):
        pass

    @abstractmethod
    def issn(self):
        pass

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
        logging.debug("text ASS")
        return self._content

    def save(self, res_file, clean=True):
        logging.debug("save : 1")
        file = open(res_file, "w")
        logging.debug("2")
        file.write(json.dumps(
            {
                self.doi_tag: self.doi(),
                self.issn_tag: self.issn(),
                self.title_tag: self.title(),
                self.abstract_tag: self.abstract(),
                self.keywords_tag: self.keywords(),
                self.text_tag: self.text()
            },
            ensure_ascii=False,
            indent=0
        ))
        logging.debug("3")
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
            basic_url = jasss_scrap_util.base_url + str(args[0]) + jasss_scrap_util.separator + str(
                args[1]) + jasss_scrap_util.separator
            req = requests.get(basic_url + str(args[2]) + jasss_scrap_util.html)
            self.url = req.url
            if req.status_code == requests.codes.ok:
                self.bs_article = BeautifulSoup(req.content, 'html5lib')
            else:
                self.bs_article = BeautifulSoup(
                    requests.get(basic_url + str("review" + args[2]) + jasss_scrap_util.html),
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

    def issn(self):
        return '1460-7425'

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

    def text(self, *args):
        """
        Text content of the article
        :param args: args[0] = boolean if true -> clean text else brut text
        :return: The plain text of the article
        """
        body = self.bs_article.findAll("article")
        if len(body) == 1:
            body = body[0].getText()
        else:
            art = self.bs_article.findAll("div", {'class': 'article'})
            if len(art) > 0:
                body = art[0].getText()
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

                body = body.getText()
        return jasss_scrap_util.remove_gif(body) if bool(args[0]) else body

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

    def __init__(self, *args):
        """
        
        """
        print("PII : ",args[0])
        self._sd_article = FullDoc(sd_pii=args[0])
        print("init SD 1")
        if not self._sd_article.read(els_client=args[1]):
            print("raise HTTPError")
            raise HTTPError
            
    def doi(self):
        """Gets the document's DOI"""
        try:
            doi = self._sd_article.data["coredata"]["dc:identifier"]
            print ("Check DOI")
            return doi_converter(doi)
        except KeyError:
            doi = ["No DOI"]
            return doi_converter(doi)
        
        
    def title(self):
        """Gets the document's title"""
        sd_title = re.sub("/"," ",self._sd_article.title)
        print ("Check title")
        return sd_title
        
    def abstract(self):
        """Gets the document's abstract"""
        return self._sd_article.data["coredata"]["dc:description"]
    
    def is_undesired(self):
        """ Tells if this article is undesired or not """
        title_revue = self.title()
        try:
            if title_revue == "Editorial Board":
                print("Editorial Board")
                return True
            if title_revue == "Index":
                print("Index")
                return True
            if "Title Page" in title_revue:
                print("Prelim Title Page")
                return True
            if "Subject Index" in title_revue:
                print("Subject Index")
                return True
            if "Letter to the Editor" in self._sd_article.data["coredata"]["pubType"]:
                print(str(self._sd_article.data["coredata"]["pubType"]))
                return True
            if "Book review" in self._sd_article.data["coredata"]["pubType"]:
                print(str(self._sd_article.data["coredata"]["pubType"]))
                return True
        except KeyError:
            return False
        
    def author_checking(self):
        try:
            if self._sd_article.data["coredata"]["dc:creator"][0]["$"] == str:
                print("find Author 1")
                return True
            if self._sd_article.data["coredata"]["dc:creator"]["$"] == str:
                print("find Author 2")
                return True
        except KeyError :
            print("No Author")
            return False
        
    def author_1(self):
        
        if self.author_checking:
            try:
                author_brut = self._sd_article.data["coredata"]["dc:creator"][0]["$"]
                print ("2",author_brut)
                author = re.sub(r'(,|\.)','',author_brut)
                print ("3",author)
                author_sub = re.sub(r'(^\w+\b \w)',"",author)
                
                print ("4")
                print (author_sub)
                author_final = re.sub(author_sub,"",author)
                print ("5",author_final)
                AUTHOR = author_final.upper()
                print ("6",AUTHOR)
                AUTHOR = unicodedata.normalize('NFD', AUTHOR).encode('ASCII', 'ignore')
                print ("7",AUTHOR)
                AUTHOR = re.sub(r'(b|\|\.|\')','',str(AUTHOR))
                print ("8")
                return AUTHOR
                
            except:
                author_brut = self._sd_article.data["coredata"]["dc:creator"]["$"]
                print("Author :",author_brut)
                author = re.sub(r'(,|\.)','',author_brut)
                author_sub = re.sub(r'(^\w+\b \w)',"",author)
                author_final = re.sub(author_sub,"",author)
                AUTHOR = author_final.upper()
                AUTHOR = unicodedata.normalize('NFD', AUTHOR).encode('ASCII', 'ignore')
                AUTHOR = re.sub(r'(b|\|\.|\')','',str(AUTHOR))
                return AUTHOR
                
           
        else:
            print("Author error")
            pass
           
            
    def concat_title(self):
        
        concat_title = self.title()
        concat_title = re.sub(r'\W','',concat_title)
        CONCAT_TITLE = concat_title.upper()
        print(CONCAT_TITLE)
        #CONCAT_TITLE = CONCAT_TITLE.encode('ASCII','ignore')
        print(CONCAT_TITLE)
        TITLE = re.sub(r'(AND|OF|THE|TO)',"",CONCAT_TITLE)
        print (TITLE)
        return TITLE
    
    def text(self):
        """Gets the document's text"""
        print("txt :1")
        txt = self._sd_article.data["originalText"]
        txt = re.sub(r' Nomenclature',"",txt)
        print("2")
        auteur = str(self.author_1())
        
        #auteur = re.sub(r'\W','',auteur)
        print("3")
        print(auteur)
        txt_1 = ".*"+auteur
        print("4")
        print(txt_1)
        print("5")
        
        
        text_1 = re.sub(txt_1,"",txt)
        text_sub = re.sub(r'(1\.1|2)\W.*','',text_1)
        #print ("\n2eme étape :",text_sub)
        
        
        if "serial JL" in text_sub:
           # print ("Syntax author")
           # title = self.concat_title()
           # print(type(title))
           # print(title)
           # title_sub = ".*{}".format(title)
           # print ("title_sub",title_sub)
           # text_brut = re.sub(r'%s'%title_sub,'',txt)
           # #print(text_brut)
           # text_brut = re.sub(r'^\D+','',text_brut)
           # print(text_brut)
           # intro = re.sub(r'(1\.1|2)(.|\n)*','',text_brut)
           # #print("\n2 :",text_brut)
           # print("\n Intro :",intro)
           # text_alone = re.sub(r'.*%s'%intro,"",txt)
            print ("Syntax author")
            return remove_gif(txt)
        
        else:
            text_alone = re.sub(r'.*%s'%text_sub,"",text_1)
            print("6")
            text_alone = re.sub(r'[^a-zA-Z0-9_ ]',"",text_alone)
            print("6,5")
            text_alone = re.sub(r'( References).*',"",text_alone)
            text_alone = re.sub(r'( Appendix A).*',"",text_alone)
            print("7")
            #cln_txt = remove_gif(txt)
            return text_alone
    
    def keywords(self):
        """Gets the document's Keywords"""
        try:    
            kw=self._sd_article.data["coredata"]["dcterms:subject"]
            KW_list = [item['$'] for item in kw]
            return KW_list
        except KeyError:
            KW_list = ["No Keyword"]
            return KW_list

