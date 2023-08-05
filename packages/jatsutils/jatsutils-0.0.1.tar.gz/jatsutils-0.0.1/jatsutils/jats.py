import xmltodict
from lxml import etree
from lxml.etree import tostring


class JatsElementTree:

    def __init__(self, from_file='', from_string=''):
        self.root = None
        if from_file:
            self.parse(from_file)
        elif from_string:
            self.fromstring(from_string)

    def parse(self, *args, **kwargs):
        """
        Loads a JATS XML file
        :param args:
        :param kwargs:
        :return: XML tree root
        """
        self.root = etree.parse(*args, **kwargs)
        return self.root

    def fromstring(self, *args, **kwargs):
        """
        Loads a JATS XML string
        :param args:
        :param kwargs:
        :return: XML tree root
        """
        self.root = etree.fromstring(*args, **kwargs)
        return self.root

    def dump(self):
        """
        Dump XML tree as string
        :return: string
        """
        return etree.tostring(self.root)

    def get_article_categories(self):
        """
        Get article categories XML representation as dict
        :return: OrderedDict
        """
        categories_tree = self.root.find('front/article-meta/article-categories')
        # return [xmltodict.parse(tostring(c)) for c in categories_tree]
        return xmltodict.parse(tostring(categories_tree))

    def get_title(self):
        """
        Get article title
        :return: string
        """
        return self.root.find('front/article-meta/title-group/article-title').text

    def get_trans_titles(self):
        """
        Get article translated titles as a "language:title" dictionary
        :return: dict
        """
        trans_titles_trees = self.root.findall('front/article-meta/title-group/trans-title-group')
        trans_titles = {}
        for trans_title_tree in trans_titles_trees:
            lang = trans_title_tree.attrib['{http://www.w3.org/XML/1998/namespace}lang']
            title_tree = trans_title_tree.find('trans-title')
            title = ''.join(title_tree.itertext())
            trans_titles[lang] = dict(title=title, **title_tree.attrib)
        return trans_titles

    def get_article_authors(self, only_persons=True):
        """
        Get article authors contribs representation as dict
        :param only_persons: Only returns contribs of type "person" (Default: True)
        :return: list
        """
        if only_persons:
            authors_contrib_group = self.root.findall(
                'front/article-meta/contrib-group[@content-type="author"]//contrib[@contrib-type="person"]')
        else:
            authors_contrib_group = self.root.findall(
                'front/article-meta/contrib-group[@content-type="author"]/contrib')
        author_contrib = []
        for authors_contrib in authors_contrib_group:
            author_contrib.append(xmltodict.parse(tostring(authors_contrib)))
        return author_contrib

    def get_article_editors(self, only_persons=True):
        """
        Get article editors contribs representation as dict
        :param only_persons: Only returns contribs of type "person" (Default: True)
        :return: list
        """
        if only_persons:
            editors_contrib_group = self.root.findall(
                'front/article-meta/contrib-group[@content-type="editor"]//contrib[@contrib-type="person"]')
        else:
            editors_contrib_group = self.root.findall(
                'front/article-meta/contrib-group[@content-type="editor"]/contrib')
        editor_contrib = []
        for editors_contrib in editors_contrib_group:
            editor_contrib.append(xmltodict.parse(tostring(editors_contrib)))
        return editor_contrib

    def get_article_affiliations(self):
        """
        Get article affiliations representation as dict
        :return: list
        """
        article_affiliations_group = self.root.findall('front/article-meta/aff')
        article_affiliations = []
        for article_affiliation in article_affiliations_group:
            parsed = xmltodict.parse(tostring(article_affiliation))
            if not(isinstance(parsed['aff']['institution'], list)):
                parsed['aff']['institution'] = [parsed['aff']['institution']]
            article_affiliations.append(parsed)
        return article_affiliations

    def get_article_publication_date(self):
        """
        Get article publication date representation as dict
        :return: OrderedDict
        """
        pubdate_root = self.root.find('front/article-meta/pub-date')
        return xmltodict.parse(tostring(pubdate_root))

    def get_volume(self):
        """
        Get article volume
        :return: string
        """
        return self.root.find('front/article-meta/volume').text

    def get_issue(self):
        """
        Get article issue
        :return: string
        """
        return self.root.find('front/article-meta/issue').text

    def get_fpage(self):
        """
        Get article begin page
        :return: string
        """
        return self.root.find('front/article-meta/fpage').text

    def get_lpage(self):
        """
        Get article end page
        :return: string
        """
        return self.root.find('front/article-meta/lpage').text

    def get_page_range(self):
        """
        Get article page range
        :return: string
        """
        return self.root.find('front/article-meta/page-range').text

    def get_article_history(self):
        """
        Get article history representation as dict
        :return: OrderedDict
        """
        history_root = self.root.find('front/article-meta/history')
        return xmltodict.parse(tostring(history_root))

    def get_article_permissions(self):
        """
        Get article permissions representation as dict
        :return: OrderedDict
        """
        permissions_root = self.root.find('front/article-meta/permissions')
        return xmltodict.parse(tostring(permissions_root))

    def get_article_abstract(self):
        """
        Get article abstract representation as dict
        :return: OrderedDict
        """
        abstract_root = self.root.find('front/article-meta/abstract')
        return xmltodict.parse(tostring(abstract_root))

    def get_article_trans_abstracts(self):
        """
        Get article translated abstracts representation as dict
        :return: list
        """
        trans_abstracts_roots = self.root.findall('front/article-meta/trans-abstract')
        trans_abstracts = []
        for trans_abstract in trans_abstracts_roots:
            trans_abstracts.append(xmltodict.parse(tostring(trans_abstract)))
        return trans_abstracts

    def get_article_keywords(self):
        """
        Get article keywords representation as dict
        :return: list
        """
        keywords_roots = self.root.findall('front/article-meta/kwd-group')
        keywords = []
        for keyword in keywords_roots:
            keywords.append(xmltodict.parse(tostring(keyword)))
        return keywords

    def get_article_funding_group(self):
        """
        Get article funding representation as dict
        :return: OrderedDict
        """
        founding_group_root = self.root.find('front/article-meta/funding-group')
        return xmltodict.parse(tostring(founding_group_root))
