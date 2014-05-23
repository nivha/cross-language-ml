
import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.crosslanguage.settings'

from wikipedia import Wikipedia as W_Orig
from wiki2plain import Wiki2Plain
from WikiUtils import GetWikipediaCategoryRecurse
from django.conf import settings



class FetcherError(Exception):
    pass


class Wikipedia(object):
    """
        Singleton implementation for Wikipedia object
        (not yet multithreaded proof)
    """

    _initiated = False
    _language = ''
    _wiki = None

    def __init__(self, language):
        if not self._initiated or language != self._language:
            self._wiki = W_Orig(language)
            self._language = language

    def article(self, article):
        return self._wiki.article(article)


class Article(object):
    """
        Container class for Article
    """
    def __init__(self, raw_article):
        self.language   = None
        self.link       = None
        self.title      = None
        self.text       = None
        self.fetched    = False

        self.parse(raw_article)

    def parse(self, raw_article):
        self.language = raw_article['pagelanguage']
        self.link = raw_article['link']
        self.title = raw_article['title']
        self.title_raw = raw_article['title_raw']

    def fetch(self):
        wiki = Wikipedia(self.language)
        s = wiki.article(self.title_raw)
        self.text = Wiki2Plain(s).text
        self.fetched = True

    def savetofile(self, path):
        if not self.fetched: raise FetcherError("Article must be fetched before saving")
        with open(path, 'w') as f:
            f.write(self.text)


class CategoryFetcher(object):
    """
        Fetch all articles in a Wikipedia Category
        Save each article to a file in the project's storage hierarchy
    """

    def __init__(self, category, language):
        self.category = category
        self.language = language

        self.articles = []

    def fetch_raw_articles(self):
        raw_articles = GetWikipediaCategoryRecurse(self.category, self.language)
        for raw_article in raw_articles:
            article = Article(raw_article)
            self.articles.append(article)

    def fetch_to_files(self):
        """
            Save all category's articles into files in the relevant place
        """
        category_base_dir = os.path.join(settings.DATA_DIR, self.language, self.category)
        if not os.path.exists(category_base_dir): os.makedirs(category_base_dir)

        self.fetch_raw_articles()
        for article in self.articles:
            path = os.path.join(category_base_dir, "{:s}.txt".format(article.title_raw))
            print path
            article.fetch()
            article.savetofile(path)


if __name__=="__main__":
    #c = CategoryFetcher("Maxwell_Medal_and_Prize_recipients", 'en')
    #c = CategoryFetcher("Institute_of_Physics", 'en')
    c = CategoryFetcher("Anexos:Estrellas", 'es')
    c.fetch_to_files()






