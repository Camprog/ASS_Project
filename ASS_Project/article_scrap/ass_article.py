import json
from abc import abstractmethod

import requests

from bs4 import BeautifulSoup
from elsapy.elsdoc import FullDoc
from requests import HTTPError

from article_scrap import ass_scrap_util

import re
import unicodedata
import biblib

import logging


log = logging.getLogger("ass")
log.setLevel(logging.INFO)


class ASSArticle:
    doi_tag = "DOI"
    issn_tag = "ISSN"
    title_tag = "TITLE"
    abstract_tag = "ABSTRACT"
    keywords_tag = "KEYWORDS"
    text_tag = "CONTENT"

    NA = "NA"

    def __init__(self, file):
        log.debug("init ASS")
        json_content = json.load(file)
        self._title = json_content[self.title_tag]
        self._abstract = json_content[self.abstract_tag]
        self._keywords = json_content[self.keywords_tag]
        self._content = json_content[self.text_tag]
        log.debug("init ASS end")

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
        return self._content

    def get_bib(self):
        """
        Turn this article into a string bibtex reference
        :return: a string representation of the article as a bib reference
        """
        a = biblib.entry_from_doi(self.doi())
        a.set_tag('author', self.author())
        a.set_tag('title',  self.title())
        a.set_tag('journal', self.journal())
        a.set_tag('year', self.year())



    def save(self, res_file):
        file = open(res_file, "w")
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
            req = requests.get(kwargs.get('url', ass_scrap_util.get_latest_url()))
            if req.status_code == requests.codes.ok:
                self.url = req.url
                self.bs_article = BeautifulSoup(req.content, 'html5lib')
            else:
                raise HTTPError(req.reason)
        else:
            basic_url = ass_scrap_util.base_url + str(args[0]) + ass_scrap_util.separator + str(
                args[1]) + ass_scrap_util.separator
            req = requests.get(basic_url + str(args[2]) + ".html")
            self.url = req.url
            if req.status_code == requests.codes.ok:
                self.bs_article = BeautifulSoup(req.content, 'html5lib')
            else:
                self.bs_article = BeautifulSoup(
                    requests.get(basic_url + str("review" + args[2]) + ".html"),
                    'html5lib')

    def __repr__(self):
        return self.url

    def is_review(self):
        """ Tells if this article is a review or not """
        return True if "review" in self.__repr__() \
                       or not ass_scrap_util.get_issue_from_url(self.__repr__())[-1].isdigit() \
            else False

    def keywords(self):
        """
        Get the key worlds from an article
        :return: a tuple made of key worlds
        """
        try:
            k = self.get_meta_content_with_tag("tags")
        except TypeError:
            balise = self.bs_article.find(string="Keywords:")
            k = balise.find_next_sibling() if balise.find_next_sibling() else balise.find_next().string
        return [x.strip() for x in k.split(',')]

    def title(self):
        """ Retrieve the title of the article """
        try:
            t = self.get_meta_content_with_tag()
        except TypeError:
            t = self.get_art_content_with_tag()
        t = self.bs_article.find("title").string if t == super().NA else t
        log.debug("Title is : "+t)
        return t

    def authors(self):
        """
        Retrieve the authors of the article
        :return: a tuple of authors
        """
        a = self.get_meta_content_with_tag("authors")
        if not a:
            a = self.get_art_content_with_tag("authors")
        return [x.strip() for x in a.split(';')]

    def abstract(self):
        """ Retrieve the abstract of the article"""
        the_abstract = super().NA
        try:
            the_abstract = self.get_meta_content_with_tag("abstract")
        except TypeError:
            if (the_abstract == super().NA) or len(the_abstract.split()) < 5:
                sub_abs = self.bs_article.find(string="Abstract")
                if sub_abs:
                    b1 = sub_abs.findNext("dd").next
                    b2 = sub_abs.findNext("dl").next
                    return str(b1).strip() if b1 else (str(b2.contents[0]).strip if len(b2) > 0 else super().NA)
                else:
                    return the_abstract
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
        return doi if doi else ass_scrap_util.get_issue_from_url(self.__repr__())

    def _text(self):
        body = self.bs_article.findAll("article")
        if len(body) == 1:
            return body[0]
        else:
            art = self.bs_article.findAll("div", {'class': 'article'})
            if len(art) > 0:
                return art[0]
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

                return body

    def text(self):
        """
        Text content of the article
        :return: The plain text of the article
        """
        html_text = self._text()
        script: BeautifulSoup.Tag = html_text.findAll("script")
        if not script:
            pass
        else:
            for s in script:
                s.extract()
                for n in s.find_next_siblings():
                    n.extract()
        bibliography: BeautifulSoup.Tag = html_text.findAll("div", {'id': 'refs'})
        log.debug("Looking for the bibilography div: "+str(bibliography))
        if not bibliography:
            pass
            # Seems that previous html scralling get ride off bibliography

            # all_h3 = html_text.findAll("h3")
            # log.debug(str(all_h3))
            # ref_tag = html_text.findAll("h3", text=ass_scrap_util.jasss_biblio_match)
            # log.debug("Match html tag for bibliography "+str(ref_tag))
            # for n in ref_tag.final_next_siblings():
            #     log.debug("Extract "+str(n)+" from the text")
            #     n.extract()
        else:
            for bib in bibliography:
                bib.extract()
        return ass_scrap_util.text_cleaner(html_text.getText())

    def get_meta_content_with_tag(self, tag="title"):
        """
        Retrieve the content of a tag as define by *beautifulsoup*
        :param string tag: the tag to find in the soup
        :return: a string representation of the content of the tag
        """
        m_name = ass_scrap_util.jasss_meta_name
        m_content = ass_scrap_util.jasss_meta_content
        if self.bs_article.find_next(ass_scrap_util.jasss_meta_tag,
                                     {ass_scrap_util.jasss_meta_name.upper(): "title"}):
            m_name = ass_scrap_util.jasss_meta_name.upper()
            m_content = ass_scrap_util.jasss_meta_content.upper()

        if isinstance(ass_scrap_util.meta[tag], str):
            meta_context = self.bs_article.find(ass_scrap_util.jasss_meta_tag,
                                                {m_name: ass_scrap_util.meta[tag]})
        else:
            for tg in ass_scrap_util.meta[tag]:
                meta_context = self.bs_article.find(ass_scrap_util.jasss_meta_tag, {m_name: tg})
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
        result = self.bs_article.find(balise, {'class': ass_scrap_util.art[tag]})
        if result is None:
            if tag == "doi":
                return "-".join([str(s) for s in self.__repr__() if s.isdigit()])
            else:
                return super().NA
        elif tag == "doi":
            result = result.contents[0].replace('DOI:', '') if result else super().NA
        return result.strip()

    def get_content_with_tag(self, tag="title"):
        """
        Retrieve the content associated with a conceptual tag that does not exist in JASSS HTML format (old artilces)
        :param tag: the part of the article to look for (default = 'title')
        :return: a string representation of requested part of the article
        """

    def get_soup(self):
        """
        
        :return: the soup of the source retrieve by *beautifulsoup* 
        """
        return self.bs_article


class ScienceDirectArticle(ASSArticle):

    def __init__(self, *args):
        """
        
        """
        print("PII : ", args[0])
        self._sd_article = FullDoc(sd_pii=args[0])
        print("init SD 1")
        if not self._sd_article.read(els_client=args[1]):
            print("raise HTTPError")
            raise HTTPError

    def doi(self):
        """Gets the document's DOI"""
        try:
            doi = self._sd_article.data["coredata"]["dc:identifier"]
            # log.info("Check DOI",doi_converter(doi))
            return ass_scrap_util.doi_converter(doi)
        except KeyError:
            doi = ["No DOI"]
            log.warning("No DOI")
            return ass_scrap_util.doi_converter(doi)

    def issn(self):
        try:
            issn = self._sd_article.data["coredata"]["prism:issn"]
            return issn
        except KeyError:
            return "No ISSN"
            
    def title(self):
        """Gets the document's title"""
        try:
            sd_title = re.sub("/", " ", self._sd_article.title)
        # log.info("Check title",sd_title)
            return sd_title
        except KeyError:
            return "No Title"

    def abstract(self):
        """Gets the document's abstract"""
        return self._sd_article.data["coredata"]["dc:description"]

    def is_undesired(self):
        """ Tells if this article is undesired or not """
        title_revue = self.title()
        try:   
            if "Erratum to" in title_revue:
                log.info("Erratum")
                return True
            if "Editorial" in title_revue:
                log.info("Editorial")
                return True
            if title_revue == "Index":
                log.info("Index")
                return True
            if "Title Page" in title_revue:
                log.info("Title page")
                return True
            if "Subject Index" in title_revue:
                log.info("Subject Index")
                return True
            if "Author Index" in title_revue:
                log.info("Author Index")
                return True
            if "Preface" in title_revue:
                log.info("Preface")
                return True
            if "Letter to the Editor" in self._sd_article.data["coredata"]["pubType"]:
                log.info(str(self._sd_article.data["coredata"]["pubType"]))
                return True
            if "Book review" in self._sd_article.data["coredata"]["pubType"]:
                log.info(str(self._sd_article.data["coredata"]["pubType"]))
                return True
            if "Author index" in title_revue:
                log.info("Author index")
                return True
            if "Editorial" in self._sd_article.data["coredata"]["pubType"]:
                log.info(str(self._sd_article.data["coredata"]["pubType"]))
                return True
            if "Short communication" in self._sd_article.data["coredata"]["pubType"]:
                log.info(str(self._sd_article.data["coredata"]["pubType"]))
                print("Short communication")
            if "Preface" in self._sd_article.data["coredata"]["pubType"]:
                log.info(str(self._sd_article.data["coredata"]["pubType"]))
                return True
            if "Corrigendum to" in title_revue:
                log.info("Corrigendum to")
                return True
            if "Announcement" in title_revue:
                log.info("Annoucement")
                return True

        except KeyError:
            return False

    def author_checking(self):
        try:
            if self._sd_article.data["coredata"]["dc:creator"][0]["$"] == str:
                log.debug("find Author 1")
                return True
            if self._sd_article.data["coredata"]["dc:creator"]["$"] == str:
                log.debug("find Author 2")
                return True
        except KeyError:
            log.warning("No Author")
            return False

    def author_1(self):

        if self.author_checking:
            try:
                author_brut = self._sd_article.data["coredata"]["dc:creator"][0]["$"]
                if author_brut:
                    log.debug("author_1: 2 "+str(author_brut))
                    author = re.sub(r'(,|\.)', '', author_brut)
                    log.debug("author_1: 3 "+str(author))
                    author_sub = re.sub(r'(^\w+\b \w)', "", author)

                    log.debug("author_1: 4 "+str(author_sub))
                    author_final = re.sub(author_sub, "", author)
                    log.debug("author_1: 5 "+str(author_final))
                    AUTHOR = author_final.upper()
                    log.debug("author_1: 6 "+str(AUTHOR))
                    AUTHOR = unicodedata.normalize('NFD', AUTHOR).encode('ASCII', 'ignore')
                    log.debug("author_1: 7 "+str(AUTHOR))
                    AUTHOR = re.sub(r'(b|\|\.|\')', '', str(AUTHOR))
                    log.debug("author_1: 8 ")
                    return AUTHOR
                else:
                    log.debug("author_1: Author -", author_brut)
                    author = re.sub(r'(,|\.)', '', author_brut)
                    author_sub = re.sub(r'(^\w+\b \w)', "", author)
                    author_final = re.sub(author_sub, "", author)
                    AUTHOR = author_final.upper()
                    AUTHOR = unicodedata.normalize('NFD', AUTHOR).encode('ASCII', 'ignore')
                    AUTHOR = re.sub(r'(b|\|\.|\')', '', str(AUTHOR))
                    return AUTHOR
            except KeyError:
                    try:
                        author_brut = self._sd_article.data["coredata"]["dc:creator"]["$"]
                        log.debug("author_1: 2 "+str(author_brut))
                        author = re.sub(r'(,|\.)', '', author_brut)
                        log.debug("author_1: 3 "+str(author))
                        author_sub = re.sub(r'(^\w+\b \w)', "", author)
                    
                        log.debug("author_1: 4 "+str(author_sub))
                        author_final = re.sub(author_sub, "", author)
                        log.debug("author_1: 5 "+str(author_final))
                        AUTHOR = author_final.upper()
                        log.debug("author_1: 6 "+str(AUTHOR))
                        AUTHOR = unicodedata.normalize('NFD', AUTHOR).encode('ASCII', 'ignore')
                        log.debug("author_1: 7 "+str(AUTHOR))
                        AUTHOR = re.sub(r'(b|\|\.|\')', '', str(AUTHOR))
                        log.debug("author_1: 8 ")
                        return AUTHOR
                    except KeyError:
                        log.warning("Author Error => KeyError")
                        return False

        else:
            log.warning("Author_checking false")
            pass

    def concat_title(self):

        concat_title = self.title()
        concat_title = re.sub(r'\W', '', concat_title)
        CONCAT_TITLE = concat_title.upper()
        log.debug("concat_title", CONCAT_TITLE)
        # CONCAT_TITLE = CONCAT_TITLE.encode('ASCII','ignore')
        TITLE = re.sub(r'(AND|OF|THE|TO)', "", CONCAT_TITLE)
        log.debug(TITLE)
        return TITLE

    def text(self):

        """Gets the document's text"""
        log.debug("text : 1")
        txt = self._sd_article.data["originalText"]
        txt = re.sub(r' Nomenclature', "", txt)
        log.debug("text : 2")
        auteur = str(self.author_1())

        # auteur = re.sub(r'\W','',auteur)
        log.debug("text : 3")
        txt_1 = ".*" + auteur
        log.debug("text : 4" + str(txt_1))

        text_1 = re.sub(r'%s' % txt_1, "", txt)
        log.debug("text : 5")

        text_sub = re.sub(r'(1\.1|2)\W.*', '', text_1)
        print (txt_1)
        # print ("\n2eme étape :",text_sub)
        
        if len(txt_1)<=5:
            
            log.warning("Fail AUTHOR => text_cleaner")
            return ass_scrap_util.text_cleaner(txt)
            
            
        if "serial JL" in text_sub :
            print("serial JL")
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
            log.warning("Syntax author => text_cleaner")
            return ass_scrap_util.text_cleaner(txt)

        else:
            text_alone = re.sub(r'.*%s'%text_sub, "", text_1)
            log.debug("text : 6")
            text_alone = re.sub(r'[^a-zA-Z0-9_ ]', "", text_alone)
            log.debug("text : 6,5")
            text_alone = ass_scrap_util.text_cleaner(text_alone)
            #text_alone = re.sub(r'(References(?!.*References)).*',' ', text_alone)
            #text_alone = re.sub(r'(Appendix(?!.*Appendix)).*',' ', text_alone)
            #clean_txt = re.sub(r'(Appendix(?!.*Appendix)).*',' ', clean_txt)
            log.debug("text : 7")
            # cln_txt = text_cleaner(txt)
            return text_alone

    
    
    def keywords(self):
        """Gets the document's Keywords"""
        try:
            kw = self._sd_article.data["coredata"]["dcterms:subject"]
            KW_list = [item['$'] for item in kw]
            return KW_list
        except KeyError:
            KW_list = "No Keyword"
            return KW_list
